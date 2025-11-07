from django.views import View
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import University, Major


# /calc/
class CalcView(View):
    def get(self, request):
        saved_calcs = {}
        if request.user.is_authenticated:
            request.user.refresh_from_db()  # Make sure we get the latest data
            saved_calcs = request.user.savedCalcs

        return render(request, 'calc/calc_page.html', {
            'saved_calcs': saved_calcs
        })

# /api/university_search
@csrf_exempt
def university_search(request):
    query = request.GET.get('query', '').strip()

    if not query:
        return JsonResponse({"universities": []}, status=400)

    universities = University.objects.filter(
        name__istartswith=query
    ).only('name', 'location').order_by('name')

    if not universities.exists():
        return JsonResponse({"universities": []}, status=404)

    data = {"universities": []}
    for uni in universities:
        data["universities"].append({
            "name": uni.name,
            "location": uni.location,
            # departments can still be included if you want, but it adds query cost
            # "departments": list(uni.majors.values_list("department", flat=True).distinct())
        })

    return JsonResponse(data)


# /api/aid/
def aid_list(request):
    uniQuery = request.GET.get('university')
    uniObj = None

    if not uniQuery:
        return HttpResponse("Error - No university provided.", status=400)

    try:
        uniObj = University.objects.get(name__iexact=uniQuery)
    except University.DoesNotExist as error:
        return HttpResponse("Error - No university found.", status=404)
    
    data = {"aids" : []}
    for aid in uniObj.applicableAids.all():
        data["aids"].append({
            'name'      : aid.name,
            'location'  : aid.location,
            'amount'    : aid.amount,
        })
    
    return JsonResponse(data)


# /api/majors/
def major_list(request):
    university_name = request.GET.get('university', '')
    department = request.GET.get('department', '')

    if not university_name:
        return HttpResponse("Error - No university provided.", status=400)

    if not department:
        return HttpResponse("Error - No department provided.", status=400)

    # Ensure university exists
    university = University.objects.filter(name__icontains=university_name).first()
    if not university:
        return HttpResponse("Error - University not found", status=404)

    # Filter majors by university and department
    majors = Major.objects.filter(university=university, department=department)
    if not majors.exists():
        return JsonResponse({"majors": []})  # Return empty list if no majors found

    data = {"majors": [{"name": major.major_name} for major in majors]}

    return JsonResponse(data)


# /api/calculate
def calculate(request):
    
    university_name = request.GET.get('university')
    major_name = request.GET.get('major')
    outstate = request.GET.get('outstate')
    aid_name = request.GET.get('aid')

    if not university_name:
        return HttpResponse("Error - No university provided.", status=400)

    if not major_name:
        return HttpResponse("Error - No major provided.", status=400)

    if not outstate:
        return HttpResponse("Error - No outstate provided.", status=400)

    # effectively cast outstate to a boolean now that we know its validated
    outstate = outstate == 'true'


    # Ensure university exists
    university = University.objects.filter(name__icontains=university_name).first()
    if not university:
        return HttpResponse("Error - University not found", status=404)

    # Ensure major exists
    major = Major.objects.filter(university=university, major_name__icontains=major_name).first()
    if not major:
        return HttpResponse("Error - Major not found", status=404)

    # Get aid
    aid = 0
    aidObj = None

    if aid_name and aid_name not in ["", "None", "null"]:
        # Try to convert to int (custom aid), else treat as aid name
        try:
            aid = int(aid_name)
        except ValueError:
            aidObj = FinancialAid.objects.filter(name=aid_name).first()
            if not aidObj:
                return HttpResponse("Error - Financial Aid not found.", status=404)
            aid = aidObj.amount

    


    # Determine correct tuition range
    if outstate:
        min_tuition = university.out_of_state_base_min_tuition + major.out_of_state_min_tuition
        max_tuition = university.out_of_state_base_max_tuition + major.out_of_state_max_tuition
    else:
        min_tuition = university.in_state_base_min_tuition + major.in_state_min_tuition 
        max_tuition = university.in_state_base_max_tuition + major.in_state_max_tuition

    # Add university and major fees
    min_tuition += university.fees + major.fees
    max_tuition += university.fees + major.fees


    # Apply Aid
    min_tuition -= aid
    max_tuition -= aid

    data = {
        "minTui": min_tuition,
        "maxTui": max_tuition,
        "uni": {
            "name": university.name,
            "baseMinTui": university.in_state_base_min_tuition if not outstate else university.out_of_state_base_min_tuition,
            "baseMaxTui": university.in_state_base_max_tuition if not outstate else university.out_of_state_base_max_tuition,
            "fees": university.fees
        },
        "major": {
            "name": major.major_name,
            "baseMinTui": major.in_state_min_tuition if not outstate else major.out_of_state_min_tuition,
            "baseMaxTui": major.in_state_max_tuition if not outstate else major.out_of_state_max_tuition,
            "fees": major.fees
        },
        "aid": (
            {} if aid_name in ["", "None", "null", None]
            else {"name": aidObj.name, "amount": aidObj.amount} if aidObj
            else {"name": f"Custom Aid (${aid})", "amount": aid}
        ),

    }

    return JsonResponse(data) 


# /api/calcs/
def calc_list(request):
    if not request.user.is_authenticated:
        # 401 - Unauthorized
        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/401
        return HttpResponse("Error - You must be logged in", status=401)
    
    user = request.user
    user.refresh_from_db()


    query = request.GET.get('query')

    # #if not query:
    # #    return HttpResponse("Error - No query provided", status=400)
    #
    # Above is commented out due to Vedal wanting all calcs to show when the
    # user clicks on the search bar.

    # lower the query so that the filtering can be case insensitive
    query = query.lower()

    # dict_you_want = {key: old_dict[key] for key in your_keys}

    # # Returns the values of the calculators matching the filtered_keys
    # filtered_keys = ["Calculator 1", "Calculator 2"]
    # calculators = {key: user.savedCalcs[key] for key in filtered_keys}
    # 
    # # Might be useful later

    # >>> lst = ['a', 'ab', 'abc', 'bac']
    # >>> [k for k in lst if 'ab' in k]
    # ['ab', 'abc']


    # Grab the saved calculators from the user:
    savedCalcs = list(user.savedCalcs.keys())
    # This converts a dict_keys to a list of strings


    # Filter by the given query:
    applicableKeys = [key for key in savedCalcs if query in key]

    data = {"calculators" : []}

    # Create a dictionary of the mix-case names to their corresponding keys
    for key in applicableKeys:
        data['calculators'].append(
            user.savedCalcs[key]
        )

    # Return the data

    # Example return data:
    #
    #   {'calculators'  :   [
    #       {
    #           'calcName'  :   'UofSC',
    #           'uni'       :   'UofSC',
    #           'outstate'  :    False,
    #           'dept'      :   'Engineering and Technology',
    #           'major'     :   'CIS',
    #           'aid'       :   'Palmetto Fellows'
    #       },
    #       {
    #           'calcName'  :   'Custom Name',
    #            ...
    #       },
    #       ...
    #   ]}
    #

    return JsonResponse(data)


# /api/save_calc
def save_calc(request):
    if not request.user.is_authenticated:
        return HttpResponse("Error - You must be logged in", status=403) # 403 Forbidden

    user = request.user

    if request.method == 'DELETE':
        # Expected Data
        #
        # { 'calcname' : { True } } // key is the name of the calculator but in lowercase
        # 
        # // The value in the json is not important, just the key is used to delete the calculator
        
        try:
            data = json.loads(request.body.decode())
            key = list(data.keys())[0].lower()

            if key in user.savedCalcs:
                del user.savedCalcs[key]
                user.save()
                return HttpResponse("Deleted", status=204) # No Content, preferred for deletions
            else: 
                return HttpResponse("Key not found", status=404)

        except Exception as e:
            return HttpResponseBadRequest("Invalid delete request: " + str(e))

    if request.method == 'POST':
        # Expected Data
        # { 'calcname'      : {      // key is the name of the calculator but in lowercase
        #        'calcName'      :   'testCalc',
        #        'uni'           :   'exampleUni',
        #        'oustate'       :    False,
        #        'dept'          :   'Humanities and Social Sciences',
        #        'major'         :   'exampleMajor',
        #        'aid'           :   'exampleAid',
        #    }
        # }


        try:
            data = json.loads(request.body.decode())
            key = list(data.keys())[0].lower() # The view "politely" corrects the key to be lowercase
            value = data[key]

            # Validate value
            if not isinstance(value, dict):
                return HttpResponseBadRequest("Invalid value format. Expected a dictionary.")
            
            # Validate required fields in the value dictionary
            required_fields = ['calcName', 'uni', 'outstate', 'dept', 'major', 'aid']
            for field in required_fields:
                if field not in value:
                    return HttpResponseBadRequest(f"Missing required field: {field}")

            # Validate that all fields are strings or booleans as appropriate
            for field in required_fields:
                if field == 'outstate':
                    if not isinstance(value[field], bool):
                        return HttpResponseBadRequest(f"Field '{field}' must be a boolean.")
                elif field == 'aid':
                    if not isinstance(value[field], (str, int)):
                        return HttpResponseBadRequest(f"Field '{field}' must be a string or an integer.")
                else:
                    if not isinstance(value[field], str):
                        return HttpResponseBadRequest(f"Field '{field}' must be a string.")

            # Save or update the calculator
            user.savedCalcs[key] = value
            user.save()
            return HttpResponse("Saved", status=201) # Created, preferred for new resources

        except Exception as e:
            return HttpResponseBadRequest("Error saving calculator: " + str(e))


    # The method was neither delete nor post, respond with 405 and an allow header with the list
    # of the supported methods

    # (mozilla wants us to do this apparently)
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Allow

    allowed_methods = "POST, DELETE"

    # return an http response with a 405 status code and the allowed methods in the header
    response = HttpResponse("Method Not Allowed", status=405)

    # Add the values in the allowed methods to the header
    response['Allow'] = allowed_methods
   
    return response