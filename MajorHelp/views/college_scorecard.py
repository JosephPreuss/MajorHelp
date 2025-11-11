import os
import requests
from django.http import JsonResponse

# Retrieve the College Scorecard API key from environment variables.
# This is for security, so the key is not hardcoded in the source code.
API_KEY = os.environ.get('COLLEGE_SCORECARD_API_KEY')
# The base URL for the College Scorecard API.
API_BASE_URL = 'https://api.data.gov/ed/collegescorecard/v1/schools'

def college_scorecard_api(request, school_name):
    """
    API endpoint to get College Scorecard data for a university.
    This view acts as a proxy to the College Scorecard API,
    simplifying the data and making it available to our frontend.
    """
    # If the API key is not configured, we can't proceed.
    # This is a server-side issue, so we return a 500 error.
    if not API_KEY:
        return JsonResponse({'error': 'API key for College Scorecard not set.'}, status=500)

    # Define the specific fields we want to retrieve from the API.
    # This reduces the amount of data transferred and keeps our API focused.
    fields_to_request = [
        'id',
        'school.name',
        'school.city',
        'school.state',
        'school.zip',
        'school.school_url',
        'latest.student.size',
        'latest.admissions.admission_rate.overall',
        'latest.admissions.sat_scores.average.overall',
        'latest.admissions.act_scores.midpoint.cumulative',
        'latest.cost.tuition.in_state',
        'latest.cost.tuition.out_of_state',
        'latest.completion.completion_rate_4yr_150nt',
        'latest.earnings.6_yrs_after_entry.mean_earnings',
        'latest.earnings.8_yrs_after_entry.median',
        'latest.earnings.10_yrs_after_entry.median',
        'latest.aid.median_debt.completers.overall',
        'latest.aid.median_debt.noncompleters',
        'latest.repayment.3_yr_repayment.repayment_rate',
        'latest.aid.pell_grant_rate',
        'latest.student.demographics.first_generation',
    ]

    # These are the parameters for our API request to the College Scorecard.
    params = {
        'api_key': API_KEY,
        'school.name': school_name,
        'fields': ','.join(fields_to_request),
        '_per_page': 1 # We only expect one result for a given school name.
    }

    try:
        # Make the request to the external API.
        response = requests.get(API_BASE_URL, params=params)
        # This will raise an exception if the API returns a non-200 status code.
        response.raise_for_status()
        data = response.json()

        # If the API returns no results, we return a 404 error.
        if not data.get('results'):
            return JsonResponse({'error': 'No data found for this school.'}, status=404)

        result = data['results'][0]

        # Re-format the messy government field names into a clean, simple JSON object.
        # This makes the data easier to work with on the frontend.
        clean_data = {
            'school_name': result.get('school.name'),
            'city': result.get('school.city'),
            'state': result.get('school.state'),
            'zip_code': result.get('school.zip'),
            'school_url': result.get('school.school_url'),
            'student_size': result.get('latest.student.size'),
            'admission_rate': result.get('latest.admissions.admission_rate.overall'),
            'sat_average': result.get('latest.admissions.sat_scores.average.overall'),
            'act_midpoint': result.get('latest.admissions.act_scores.midpoint.cumulative'),
            'tuition_in_state': result.get('latest.cost.tuition.in_state'),
            'tuition_out_of_state': result.get('latest.cost.tuition.out_of_state'),
            'completion_rate': result.get('latest.completion.completion_rate_4yr_150nt'),
            'mean_earnings_6_yrs_after_entry': result.get('latest.earnings.6_yrs_after_entry.mean_earnings'),
            'median_earnings_8_yrs_after_entry': result.get('latest.earnings.8_yrs_after_entry.median'),
            'median_earnings_10_yrs_after_entry': result.get('latest.earnings.10_yrs_after_entry.median'),
            'median_debt_completers': result.get('latest.aid.median_debt.completers.overall'),
            'median_debt_noncompleters': result.get('latest.aid.median_debt.noncompleters'),
            'repayment_rate_3_yr': result.get('latest.repayment.3_yr_repayment.repayment_rate'),
            'pell_grant_rate': result.get('latest.aid.pell_grant_rate'),
            'first_generation_students': result.get('latest.student.demographics.first_generation'),
        }

        return JsonResponse(clean_data)

    except requests.exceptions.RequestException as e:
        # If the request to the external API fails, we return a 500 error.
        return JsonResponse({'error': f'API request failed: {e}'}, status=500)
