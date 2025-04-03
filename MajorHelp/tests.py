from django.test import TestCase

from django.test import Client

from django.urls import reverse

from django.contrib.auth import get_user_model

import json

from .models import *


# Create your tests here.

class RequestTests(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.url = reverse("MajorHelp:university-request")

    def testUniversityRequestViewGET(self):
        response = self.client.get(self.url)

        # check status code
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response['content-type'], 'text/html; charset=utf-8')

    def testUniversityRequestViewPOST(self):
        name = "testUni"

        post = self.client.post(self.url, {'request_text': name})

        self.assertEqual(post.status_code, 302)

        # Assert that a request was put into the database
        
        self.assertTrue(UniversityRequest.objects.filter(request_text=name).exists())
        



class CalcTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username='testuser', password='password', email="email@example.com")
        exampleAid = FinancialAid.objects.create(name="exampleAid") 
        exampleUni = University.objects.create(name="exampleUni")

        exampleUni.applicableAids.add(exampleAid)

        Major.objects.create(
            major_name="exampleMajor", slug="exampleMajor", university=exampleUni,
            department='Humanities and Social Sciences'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = reverse("MajorHelp:calc")
        self.uni = reverse("MajorHelp:university_search")
        self.maj = reverse("MajorHelp:major_list")
        self.aid = reverse("MajorHelp:aid_list")
        self.cal = reverse("MajorHelp:calculate")
        self.sav = reverse("MajorHelp:save_calc")

        self.calcJson = {
            'calcname'      : {
                'calcName'      :   'testCalc',
                'uni'           :   'exampleUni',
                'outstate'       :   False,
                'dept'          :   'Humanities and Social Sciences',
                'major'         :   'exampleMajor',
                'aid'           :   'exampleAid',
            }
        }

    # ========================= Calc Page ====================================

    # A simple test to make sure that the server returns the proper html page
    # whenever /calc/ is accessed.
    def testCalcNoDataEntry(self):
        response = self.client.get(self.url)

        # check status code
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response['content-type'], 'text/html; charset=utf-8')
    
    def test_authenticated_user_sees_calc_panel(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create, save, and load calculations here.')

    def test_unauthenticated_user_sees_login_prompt(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Log In')
        self.assertContains(response, 'Sign Up')

    def test_panel_expand_and_collapse(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(self.url)
        self.assertContains(response, 'Expand.')
        self.assertContains(response, 'Hide.')

    def test_new_calculator_creation(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(self.url)
        self.assertContains(response, 'New Calculator')

    def test_notification_hidden_by_default(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(self.url)
        self.assertContains(response, 'id="notification"')
        self.assertContains(response, 'style="display: none;"')

    # ========================== Saving and Deleting ==========================

    # Saves

    def testSaveCalc(self):
        self.client.login(username='testuser', password='password')

        # CSRF cookies are automatically disabled in test cases,
        # so they don't need to be included in the post request.
        response = self.client.post(self.sav, json.dumps(self.calcJson), content_type='application/json')

        print(response.content)

        # Assert that the server responded with a successful creation
        self.assertEqual(response.status_code, 201)

    def testSaveCalcNoData(self):
        self.client.login(username='testuser', password='password')

        response = self.client.post(self.sav)

        # Assert that the server responded with a bad request
        self.assertEqual(response.status_code, 400)

    def testSaveCalcNotLoggedIn(self):
        response = self.client.post(self.sav)

        # Assert that the server responded with a bad request
        self.assertEqual(response.status_code, 403)

    def testSaveCalcInvalidData(self):
        self.client.login(username='testuser', password='password')

        # CSRF cookies are automatically disabled in test cases,
        # so they don't need to be included in the post request.
        response = self.client.post(self.sav, json.dumps({}), content_type='application/json')

        print(response.content)

        # Assert that the server responded with a bad request
        self.assertEqual(response.status_code, 400)

    def testSaveCalcInvalidData2(self):
        self.client.login(username='testuser', password='password')

        # CSRF cookies are automatically disabled in test cases,
        # so they don't need to be included in the post request.
        response = self.client.post(self.sav, json.dumps({"calcname": 1}), content_type='application/json')

        print(response.content)

        # Assert that the server responded with a bad request
        self.assertEqual(response.status_code, 400)
    
    def testSaveCalcInvalidData3(self):
        self.client.login(username='testuser', password='password')

        # CSRF cookies are automatically disabled in test cases,
        # so they don't need to be included in the post request.
        response = self.client.post(self.sav, json.dumps(
            {"calcname": {}}), content_type='application/json')

        print(response.content)

        # Assert that the server responded with a bad request
        self.assertEqual(response.status_code, 400)

    def testSaveCalcInvalidData4(self):
        self.client.login(username='testuser', password='password')

        # CSRF cookies are automatically disabled in test cases,
        # so they don't need to be included in the post request.
        response = self.client.post(self.sav, json.dumps(
            {"calcname": {
                "calcName": 1
            }}), content_type='application/json')

        print(response.content)

        # Assert that the server responded with a bad request
        self.assertEqual(response.status_code, 400)
    
    def testSaveCalcInvalidData5(self):
        self.client.login(username='testuser', password='password')

        # CSRF cookies are automatically disabled in test cases,
        # so they don't need to be included in the post request.
        response = self.client.post(self.sav, json.dumps({"calcname": {"calcName": "testCalc"}}), content_type='application/json')

        print(response.content)

        # Assert that the server responded with a bad request
        self.assertEqual(response.status_code, 400)

    def testSaveCalcInvalidData6(self):
        self.client.login(username='testuser', password='password')

        # CSRF cookies are automatically disabled in test cases,
        # so they don't need to be included in the post request.
        response = self.client.post(self.sav, json.dumps(
            {"calcname": {
                "calcName": "testCalc",
                "uni": 1
            }}), content_type='application/json')

        print(response.content)

        # Assert that the server responded with a bad request
        self.assertEqual(response.status_code, 400)

    def testSaveCalcInvalidData7(self):
        self.client.login(username='testuser', password='password')

        # CSRF cookies are automatically disabled in test cases,
        # so they don't need to be included in the post request.
        response = self.client.post(self.sav, json.dumps(
            {"calcname": {
                "calcName": "testCalc",
                "uni": "exampleUni",
                "outstate": 1
            }}), content_type='application/json')

        print(response.content)

        # Assert that the server responded with a bad request
        self.assertEqual(response.status_code, 400)

    def testSaveCalcInvalidData8(self):
        self.client.login(username='testuser', password='password')

        # CSRF cookies are automatically disabled in test cases,
        # so they don't need to be included in the post request.
        response = self.client.post(self.sav, json.dumps(
            {"calcname": {
                "calcName": "testCalc",
                "uni": "exampleUni",
                "outstate": False, 
                "dept": 1
            }}), content_type='application/json')

        print(response.content)

        # Assert that the server responded with a bad request
        self.assertEqual(response.status_code, 400)
    
    def testSaveCalcInvalidData9(self):
        self.client.login(username='testuser', password='password')

        # CSRF cookies are automatically disabled in test cases,
        # so they don't need to be included in the post request.
        response = self.client.post(self.sav, json.dumps(
            {"calcname": {
                "calcName": "testCalc",
                "uni": "exampleUni",
                "outstate": False,
                "dept": "Humanities and Social Sciences",
                "major": 1
            }}), content_type='application/json')

        print(response.content)

        # Assert that the server responded with a bad request
        self.assertEqual(response.status_code, 400)
    
    def testSaveCalcInvalidData10(self):
        self.client.login(username='testuser', password='password')

        # CSRF cookies are automatically disabled in test cases,
        # so they don't need to be included in the post request.
        response = self.client.post(self.sav, json.dumps(
            {"calcname": {
                "calcName": "testCalc",
                "uni": "exampleUni",
                "outstate": False,
                "dept": "Humanities and Social Sciences",
                "major": "exampleMajor",
                "aid": 1
            }}), content_type='application/json')

        print(response.content)

        # Assert that the server responded with a bad request
        self.assertEqual(response.status_code, 400)

    # Deletions

    def testDeleteCalc(self):
        self.client.login(username='testuser', password='password')

        # first save the calc to the database
        response1 = self.client.post(self.sav, json.dumps(self.calcJson), content_type='application/json')

        self.assertEqual(response1.status_code, 201)

        # then delete it
        response2 = self.client.delete(self.sav, json.dumps({'calcname' : True }), content_type='application/json')

        self.assertEqual(response2.status_code, 204)

    def testDeleteCalcNoData(self):
        self.client.login(username='testuser', password='password')

        # first save the calc to the database
        response1 = self.client.post(self.sav, json.dumps(self.calcJson), content_type='application/json')

        self.assertEqual(response1.status_code, 201)

        # then delete it
        response2 = self.client.delete(self.sav)

        self.assertEqual(response2.status_code, 400)

    def testDeleteCalcNotLoggedIn(self):
        self.client.login(username='testuser', password='password')

        # first save the calc to the database
        response1 = self.client.post(self.sav, json.dumps(self.calcJson), content_type='application/json')

        self.assertEqual(response1.status_code, 201)

        # Log out the user
        self.client.logout()

        # then delete it
        response2 = self.client.delete(self.sav)

        self.assertEqual(response2.status_code, 403)

    def testDeleteCalcInvalidData(self):
        self.client.login(username='testuser', password='password')

        # first save the calc to the database
        response1 = self.client.post(self.sav, json.dumps(self.calcJson), content_type='application/json')

        self.assertEqual(response1.status_code, 201)

        # then delete it
        response2 = self.client.delete(self.sav, json.dumps({}), content_type='application/json')

        print(response2.content)

        # Assert that the server responded with a bad request
        self.assertEqual(response2.status_code, 400)

    # Other request methods
    def testCalcGetRequest(self):
        self.client.login(username='testuser', password='password')

        response = self.client.get(self.sav)

        # Assert that the server responded with a bad request
        self.assertEqual(response.status_code, 405)

        # Check that the server responded with an allow header specifying DELETE or POST
        self.assertEqual(response['Allow'], 'POST, DELETE')

    def testCalcPutRequest(self):
        self.client.login(username='testuser', password='password')

        response = self.client.put(self.sav)

        # Assert that the server responded with a bad request
        self.assertEqual(response.status_code, 405)

        # Check that the server responded with an allow header specifying DELETE or POST
        self.assertEqual(response['Allow'], 'POST, DELETE')
    
    def testCalcPatchRequest(self):
        self.client.login(username='testuser', password='password')

        response = self.client.patch(self.sav)

        # Assert that the server responded with a bad request
        self.assertEqual(response.status_code, 405)

        # Check that the server responded with an allow header specifying DELETE or POST
        self.assertEqual(response['Allow'], 'POST, DELETE')
    
    def testCalcOptionsRequest(self):
        self.client.login(username='testuser', password='password')

        response = self.client.options(self.sav)

        # Assert that the server responded with a bad request
        self.assertEqual(response.status_code, 405)

        # Check that the server responded with an allow header specifying DELETE or POST
        self.assertEqual(response['Allow'], 'POST, DELETE')
    
    def testCalcHeadRequest(self):
        self.client.login(username='testuser', password='password')

        response = self.client.head(self.sav)

        # Assert that the server responded with a bad request
        self.assertEqual(response.status_code, 405)

        # Check that the server responded with an allow header specifying DELETE or POST
        self.assertEqual(response['Allow'], 'POST, DELETE')
    
    def testCalcTraceRequest(self):
        self.client.login(username='testuser', password='password')

        response = self.client.trace(self.sav)

        # Assert that the server responded with a bad request
        self.assertEqual(response.status_code, 405)

        # Check that the server responded with an allow header specifying DELETE or POST
        self.assertEqual(response['Allow'], 'POST, DELETE')
    
    # ========================= University Search =============================


    # The typical use case for the university search
    def testUniversitySearch(self):
        getData = "?query=exampleUni"

        response = self.client.get(self.uni+getData)

        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(response['content-type'], 'application/json')

        data = json.loads(response.content)

        self.assertEqual(data["universities"][0]["name"], "exampleUni")

    # The api should return a 400 error if no query was provided
    def testUniversitySearchNoQuery(self):

        response = self.client.get(self.uni)

        self.assertEqual(response.status_code, 400)

    # Likewise, it should return 400 if the query is empty
    def testUniversitySearchEmptyQuery(self):
        getData = "?query="

        response = self.client.get(self.uni+getData)

        self.assertEqual(response.status_code, 400)

    # The api should return a 404 error if a non existient university was provided
    def testUniversitySearchNoUniversity(self):
        getData = "?query=DoesntExistU"

        response = self.client.get(self.uni+getData)

        self.assertEqual(response.status_code, 404)


    # ========================= Major List ====================================


    # The typical use case for the major List
    def testMajorList(self):
        getData = "?university=exampleUni&department=Humanities+and+Social+Sciences"

        response = self.client.get(self.maj+getData)

        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(response['content-type'], 'application/json')

        data = json.loads(response.content)

        self.assertEqual(data["majors"][0]["name"], "exampleMajor")

    # The api should return a 400 error if nothing was provided
    def testMajorListNoUniversityOrDept(self):

        response = self.client.get(self.maj)

        self.assertEqual(response.status_code, 400)

    def testMajorListNoUniversity(self):
        getData = "?department=Humanities+and+Social+Sciences"

        response = self.client.get(self.maj+getData)

        self.assertEqual(response.status_code, 400)

    # Likewise, it should return 400 if the query is empty
    def testMajorListEmptyUniversity(self):
        getData = "?University=&department=Humanities+and+Social+Sciences"

        response = self.client.get(self.maj+getData)

        self.assertEqual(response.status_code, 400)

    def testMajorListNoDepartment(self):
        getData = "?university=exampleUni"

        response = self.client.get(self.maj+getData)

        self.assertEqual(response.status_code, 400)

    # Likewise, it should return 400 if the query is empty
    def testMajorListEmptyDepartment(self):
        getData = "?university=exampleUni&department="

        response = self.client.get(self.maj+getData)

        self.assertEqual(response.status_code, 400)

    # The api should return a 404 error if a non existient University was provided
    def testMajorListNonExistUniversity(self):
        getData = "?university=DoesntExistU&department=Humanities+and+Social+Sciences"

        response = self.client.get(self.maj+getData)

        self.assertEqual(response.status_code, 404)


    # ========================== Aid List =====================================


    # The typical use case for the aid list
    def testAidList(self):
        getData = "?university=exampleUni"

        response = self.client.get(self.aid+getData)

        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(response['content-type'], 'application/json')

        data = json.loads(response.content)

        self.assertEqual(data["aids"][0]["name"], "exampleAid")

    # The api should return a 400 error if no university was provided
    def testAidListNoQuery(self):

        response = self.client.get(self.aid)

        self.assertEqual(response.status_code, 400)

    # Likewise, it should return 400 if the query is empty
    def testAidListEmptyQuery(self):
        getData = "?university="

        response = self.client.get(self.aid+getData)

        self.assertEqual(response.status_code, 400)

    # The api should return a 404 error if a non existient university was provided
    def testAidListNoUniversity(self):
        getData = "?university=DoesntExistU"

        response = self.client.get(self.aid+getData)

        self.assertEqual(response.status_code, 404)


    # ========================== calculator =====================================


    # The typical use case for the calculator
    def testCalc(self):

        getData = "?university=exampleUni&major=exampleMajor&outstate=false"

        response = self.client.get(self.cal+getData)

        self.assertEqual(response.status_code, 200)
    
        # data = json.loads(response.content)

        # print(data)

        self.assertEqual(response['content-type'], 'application/json')

    def testCalcWithAid(self):

        getData = "?university=exampleUni&major=exampleMajor&outstate=false&aid=exampleAid"

        response = self.client.get(self.cal+getData)

        self.assertEqual(response.status_code, 200)
    

        self.assertEqual(response['content-type'], 'application/json')

        data = json.loads(response.content)

        # print(data)

        self.assertEqual(data['aid']['name'], "exampleAid")
    
    def testCalcNoQuery(self):
        response = self.client.get(self.cal)

        self.assertEqual(response.status_code, 400)



#  unit test for University Ratings Model
class UniRatingsTests(TestCase):
    def setUp(self):
    # Create test users
        self.user = CustomUser.objects.create_user(
            username="testuser",
            password="testpassword",
            email="testuser@example.com",
        )

        self.user2 = CustomUser.objects.create_user(
            username="testuser2",
            password="testpassword",
            email="testuser2@example.com",
        )
        
        self.user3 = CustomUser.objects.create_user(
            username="testuser3",
            password="testpassword",
            email="testuser3@example.com",
        )

        # Create a test university
        self.university = University.objects.create(
            name="Test University",
            location="Test City, Test State",
            is_public=True,
            aboutText="This is a test university.",
        )

        # Create unique ratings
        UniversityRating.objects.create(
            university=self.university,
            category="campus",
            rating=4.0,
            user=self.user,
        )
        UniversityRating.objects.create(
            university=self.university,
            category="campus",
            rating=5.0,
            user=self.user2,  # Different user
        )
        UniversityRating.objects.create(
            university=self.university,
            category="safety",
            rating=3.0,
            user=self.user,  # Different category
    )

    def test_get_average_rating(self):
        # Test the average rating for "campus"
        campus_avg = self.university.get_average_rating("campus")
        self.assertEqual(campus_avg, 4.5)  # Average of 4.0, 5.0, and 3.0
        
        saftey_avg = self.university.get_average_rating("safety")
        self.assertEqual(saftey_avg, 3.0)

     
#  unit test for user role assignment
    class UserRoleAssignmentTest(TestCase):
        def setUp(self):
            # creating two users with different roles 
            self.alumni_user = CustomUser.objects.create_user (
                username='alumni_user',
                password='alumnipassword123',
                role='alumni',
                email='alumni@example.com'
            )
            self.current_student_user = CustomUser.objects.create_user(
            username='current_student_user',
            password='current_studentpassword123',
            role='current_student',
            email='currentstudent@example.com'
        )
            
        def test_user_roles(self):
            # Fetch users from the database
            alumni_user = CustomUser.objects.get(username='alumni_user')
            current_student_user = CustomUser.objects.get(username='current_student_user')

            # Checks if roles are assigned correctly
            self.assertEqual(alumni_user.role, 'alumni')
            self.assertEqual(current_student_user.role, 'current_student')

            # Ensures the user data is consistent 
            self.assertTrue(alumni_user.check_password('alumnipassword123'))
            self.assertTrue(current_student_user.check_password('current_studentpassword123'))
        
class MajorMoDELETEst(TestCase):
    def setUp(self):
        # Create a University object
        university = University.objects.create(
            name="Test University",
            location="Test City, TC",
            is_public=True,
            aboutText="A test university for testing purposes.",
            TotalUndergradStudents=10000,
            TotalGradStudents=2000,
            GraduationRate=85.5,
        )
        
        # Create a Major object
        self.major = Major.objects.create(
            university=university,
            major_name="Computer Science",
            major_description="A major focused on computer science concepts.",
            department="Engineering and Technology",
            in_state_min_tuition=5000,
            in_state_max_tuition=15000,
            out_of_state_min_tuition=20000,
            out_of_state_max_tuition=30000,
            fees=1500,
            grad_in_state_min_tuition=10000,
            grad_in_state_max_tuition=20000,
            grad_out_of_state_min_tuition=25000,
            grad_out_of_state_max_tuition=35000,
        )
        
        # Create Course objects linked to the Major
        self.course1 = Course.objects.create(
            major=self.major,
            course_name="Introduction to Programming"
        )

        self.course2 = Course.objects.create(
            major=self.major,
            course_name="Data Structures"
        )

        # Explicitly add the courses to the Major's courses relationship
        self.major.courses.add(self.course1, self.course2)

    def test_major_has_courses(self):
        # Ensure that the courses are correctly associated with the Major
        self.assertEqual(self.major.courses.count(), 2)
        self.assertIn(self.course1, self.major.courses.all())
        self.assertIn(self.course2, self.major.courses.all())

    
class SignupTest(TestCase):
    def setUp(self):
        self.url = reverse('MajorHelp:signup')  # Replace with the actual name of your signup URL if different

    def test_signup_page_renders(self):
        """
        Test that the sign-up page renders successfully.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')  # Ensure this matches your template

    def test_successful_signup(self):
        """
        Test that a new user is created with valid data.
        """
        user_data = {
            'username': 'newuser',
            'password': 'securepassword123',
            'confirm_password': 'securepassword123',
            'email': 'newuser@example.com',
            'role': 'alumni'
        }
        response = self.client.post(self.url, user_data)

        # Check for redirect (successful signup redirects).
        self.assertEqual(response.status_code, 302)  # Redirect to home or another success URL.
        
        # Check if the user exists in the database.
        self.assertTrue(CustomUser.objects.filter(username='newuser').exists())


class LoginTest(TestCase):
    def setUp(self):
        # Create a test user with the necessary data
        self.username = "testuser"
        self.password = "securepassword123"
        self.user_data = {
            'username': self.username,
            'password': self.password,
            'confirm_password': self.password,
            'email': "testuser@example.com",
            'role': 'alumni' 
        }
        
        # Use CustomUserCreationForm or your own user creation logic here
        self.user = CustomUser.objects.create_user(
            username=self.username,
            password=self.password,
            email=self.user_data['email'],
            role=self.user_data['role']
        )

        self.url = reverse('MajorHelp:login')  

    def test_login_page_renders(self):
        """
        Test that the login page renders successfully.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')  # Adjust this if needed

    def test_successful_login(self):
        """
        Test that a user can log in with correct credentials.
        """
        response = self.client.post(self.url, {
            'username': self.username,
            'password': self.password,
        })

        # After successful login, ensure it redirects (or go to dashboard/home, adjust the URL as needed)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('MajorHelp:home'))  # Adjust if the redirect target is different

