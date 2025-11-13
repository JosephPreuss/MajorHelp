import os
import requests
from django.http import JsonResponse
from difflib import SequenceMatcher

# Retrieve the College Scorecard API key from environment variables.
# This is for security, so the key is not hardcoded in the source code.
API_KEY = os.environ.get('COLLEGE_SCORECARD_API_KEY')

# The base URL for the College Scorecard API.
API_BASE_URL = 'https://api.data.gov/ed/collegescorecard/v1/schools'

def find_best_school_match(search_name, results):
    """
    Find the best matching school from API results.
    Prioritizes exact matches, then falls back to similarity scoring.

    Args:
        search_name: The school name we're searching for
        results: List of school results from the API

    Returns:
        The best matching school dict, or None if no good match found
    """
    if not results:
        return None

    # Normalize the search name for comparison
    search_name_normalized = search_name.lower().strip()

    # First, try to find an exact match
    for school in results:
        school_name = school.get('school.name', '')
        if school_name.lower().strip() == search_name_normalized:
            return school

    # If no exact match, find the school with highest similarity score
    # using difflib's SequenceMatcher for fuzzy matching
    best_match = None
    best_score = 0

    for school in results:
        school_name = school.get('school.name', '')
        # Calculate similarity ratio (0.0 to 1.0)
        similarity = SequenceMatcher(None, search_name_normalized, school_name.lower()).ratio()

        if similarity > best_score:
            best_score = similarity
            best_match = school

    # Only return a match if similarity is above 0.6 (60% similar)
    # This prevents returning completely unrelated schools
    if best_score >= 0.6:
        return best_match

    return None

def college_scorecard_api(request, school_name):
    """
    API endpoint to get College Scorecard data for a university.
    This view acts as a proxy to the College Scorecard API,
    simplifying the data and making it available to our frontend.

    Uses a two-step process:
    1. Search by name to find potential matches
    2. Select best match and fetch detailed data by ID
    """
    # If the API key is not configured, we can't proceed.
    # This is a server-side issue, so we return a 500 error.
    if not API_KEY:
        return JsonResponse({'error': 'API key for College Scorecard not set.'}, status=500)

    try:
        # STEP 1: Search for the school by name to get potential matches
        search_params = {
            'api_key': API_KEY,
            'school.name': school_name,
            'school.operating': 1,  # Only get operating schools
            'fields': 'id,school.name,school.city,school.state',
            'per_page': 20  # Get more results for better matching
        }

        search_response = requests.get(API_BASE_URL, params=search_params)
        search_response.raise_for_status()
        search_data = search_response.json()

        if not search_data.get('results'):
            return JsonResponse({
                'error': 'No schools found matching that name.',
                'searched_for': school_name
            }, status=404)

        # Find the best matching school from the results
        best_match = find_best_school_match(school_name, search_data['results'])

        if not best_match:
            return JsonResponse({
                'error': 'No good match found for that school name.',
                'searched_for': school_name,
                'suggestions': [
                    {
                        'name': school.get('school.name'),
                        'city': school.get('school.city'),
                        'state': school.get('school.state')
                    }
                    for school in search_data['results'][:5]
                ]
            }, status=404)

        school_id = best_match.get('id')

        # STEP 2: Fetch detailed data for the matched school using its ID
        # Define the specific fields we want to retrieve from the API.
        fields_to_request = [
            'id',
            'school.name',
            'school.city',
            'school.state',
            'school.zip',
            'school.school_url',
            'school.operating',
            'latest.student.size',
            'latest.admissions.admission_rate.overall',
            'latest.admissions.sat_scores.average.overall',
            'latest.admissions.act_scores.midpoint.cumulative',
            'latest.cost.tuition.in_state',
            'latest.cost.tuition.out_of_state',
            'latest.completion.completion_rate_4yr_150nt',
            # Earnings field names (6 and 10 year use .median, 8 year uses .median_earnings - API inconsistency)
            'latest.earnings.6_yrs_after_entry.median',
            'latest.earnings.8_yrs_after_entry.median_earnings',
            'latest.earnings.10_yrs_after_entry.median',
            # Debt fields (completers has .overall suffix, noncompleters does not - API inconsistency)
            'latest.aid.median_debt.completers.overall',
            'latest.aid.median_debt.noncompleters',
            # Aid and demographics
            'latest.aid.pell_grant_rate',
            'latest.student.demographics.first_generation',
        ]

        detail_params = {
            'api_key': API_KEY,
            'id': school_id,
            'fields': ','.join(fields_to_request)
        }

        detail_response = requests.get(API_BASE_URL, params=detail_params)
        detail_response.raise_for_status()
        detail_data = detail_response.json()

        if not detail_data.get('results'):
            return JsonResponse({
                'error': 'Could not fetch details for matched school.',
                'school_id': school_id
            }, status=404)

        result = detail_data['results'][0]

        # Helper function to safely convert decimal rates to percentages
        def format_rate(value):
            """Convert decimal rate (0-1) to percentage for display."""
            if value is None:
                return None
            try:
                return round(float(value) * 100, 2)
            except (ValueError, TypeError):
                return None

        # Helper function to safely get numeric values
        def safe_numeric(value):
            """Return numeric value or None."""
            if value is None:
                return None
            try:
                return float(value) if isinstance(value, (int, float)) else None
            except (ValueError, TypeError):
                return None

        # Re-format the messy government field names into a clean, simple JSON object.
        # This makes the data easier to work with on the frontend.
        clean_data = {
            'school_id': result.get('id'),
            'school_name': result.get('school.name'),
            'city': result.get('school.city'),
            'state': result.get('school.state'),
            'zip_code': result.get('school.zip'),
            'school_url': result.get('school.school_url'),
            'is_operating': result.get('school.operating') == 1,

            # Student enrollment
            'student_size': safe_numeric(result.get('latest.student.size')),

            # Admissions data - convert rates to percentages
            'admission_rate_decimal': safe_numeric(result.get('latest.admissions.admission_rate.overall')),
            'admission_rate_percentage': format_rate(result.get('latest.admissions.admission_rate.overall')),
            'sat_average': safe_numeric(result.get('latest.admissions.sat_scores.average.overall')),
            'act_midpoint': safe_numeric(result.get('latest.admissions.act_scores.midpoint.cumulative')),

            # Cost data
            'tuition_in_state': safe_numeric(result.get('latest.cost.tuition.in_state')),
            'tuition_out_of_state': safe_numeric(result.get('latest.cost.tuition.out_of_state')),

            # Completion rates - convert to percentages
            'completion_rate_decimal': safe_numeric(result.get('latest.completion.completion_rate_4yr_150nt')),
            'completion_rate_percentage': format_rate(result.get('latest.completion.completion_rate_4yr_150nt')),

            # Earnings data (FIXED: 6/10 year use .median, 8 year uses .median_earnings due to API inconsistency)
            'median_earnings_6_yrs_after_entry': safe_numeric(result.get('latest.earnings.6_yrs_after_entry.median')),
            'median_earnings_8_yrs_after_entry': safe_numeric(result.get('latest.earnings.8_yrs_after_entry.median_earnings')),
            'median_earnings_10_yrs_after_entry': safe_numeric(result.get('latest.earnings.10_yrs_after_entry.median')),

            # Debt data (completers has .overall suffix, noncompleters does not - API inconsistency)
            'median_debt_completers': safe_numeric(result.get('latest.aid.median_debt.completers.overall')),
            'median_debt_noncompleters': safe_numeric(result.get('latest.aid.median_debt.noncompleters')),

            # Aid and demographics - convert rates to percentages
            'pell_grant_rate_decimal': safe_numeric(result.get('latest.aid.pell_grant_rate')),
            'pell_grant_rate_percentage': format_rate(result.get('latest.aid.pell_grant_rate')),
            'first_generation_students_decimal': safe_numeric(result.get('latest.student.demographics.first_generation')),
            'first_generation_students_percentage': format_rate(result.get('latest.student.demographics.first_generation')),

            # Metadata for debugging
            'searched_for': school_name,
            'total_search_results': len(search_data['results']),
            'match_quality': 'exact' if best_match.get('school.name', '').lower() == school_name.lower() else 'fuzzy'
        }

        return JsonResponse(clean_data)

    except requests.exceptions.RequestException as e:
        # If the request to the external API fails, we return a 500 error.
        return JsonResponse({'error': f'API request failed: {e}'}, status=500)
