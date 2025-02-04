from django.test import TestCase

from django.test import Client

from django.urls import reverse

from django.contrib.auth import get_user_model

import json

from .models import *


# Create your tests here.

class CalcTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        exampleUni = University.objects.create(name="exampleUni")
        Major.objects.create(major_name="exampleMajor", slug="exampleMajor", university=exampleUni)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.url = reverse("MajorHelp:calc")
        self.infoUrl = reverse("MajorHelp:calcInfo")
        self.DNE = "DOESNOTEXIST"


    # A simple test to make sure that the server returns the proper html page
    # whenever /calc/ is accessed.
    def testCalcNoDataEntry(self):
        response = self.client.get(self.url)

        # check status code
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response['content-type'], 'text/html; charset=utf-8')


    # While /calc/info is meant for the frontend of the calculator to interface
    # via a GET request, it is possible to do a GET request without submitting
    # any data.. like accessing the url directly on your browser!
    #
    # To save the user some confusion, in the case where no GET data is
    # provided, the backend should just redirect to /calc/
    def testCalcInfoNoDataEntry(self):
        # follow = True makes it so that the request will follow any change,
        # ie a redirect
        response = self.client.get(self.infoUrl, follow=True)

        # This method also implicitly checks to see 
        # if the final response is 200
        self.assertRedirects(response, self.url)

    def testCalcInfoFull(self):
        getData = "?uni=exampleUni&outstate=true&dept=exampleDept&major=exampleMajor&aid="

        response = self.client.get(self.infoUrl+getData)

        # check status code
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response['content-type'], 'application/json')
    


    def testCalcInfoReturns400whenUniIsnull(self):
        
        getData = "?outstate=false&dept=A&major=exampleMajor&aid="

        response = self.client.get(self.infoUrl+getData)

        self.assertEqual(response.status_code,400)


    def testCalcInfoReturns400whenUniIsBlank(self):
                
        getData = "?uni=&outstate=false&dept=A&major=exampleMajor&aid="

        response = self.client.get(self.infoUrl+getData)

        self.assertEqual(response.status_code,400)


    # In the case where the frontend submits an entry that doesn't exist,
    # the backend should return "DOESNOTEXIST" for the entry, but otherwise not
    # error.
    def testCalcInfoNonExistientUni(self):
        # The university in this doesn't exist in the test database!
        getData = "?uni=nonExistientUni&outstate=true&dept=exampleDept&major=exampleMajor&aid="

        response = self.client.get(self.infoUrl+getData)

        # The status code should still be 200
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response['content-type'], 'application/json')

        data = json.loads(response.content)

        self.assertEqual(data["uni"]["name"], self.DNE)




    def testCalcInfoReturns400whenMajorIsnull(self):
        
        getData = "?uni=exampleUnioutstate=false&dept=A&aid="

        response = self.client.get(self.infoUrl+getData)

        self.assertEqual(response.status_code,400)


    def testCalcInfoReturns400whenMajorIsBlank(self):
                
        getData = "?uni=exampleUnioutstate=false&major=&dept=A&aid="

        response = self.client.get(self.infoUrl+getData)

        self.assertEqual(response.status_code,400)


    # In the case where the frontend submits an entry that doesn't exist,
    # the backend should return "DOESNOTEXIST" for the entry, but otherwise not
    # error.
    def testCalcInfoNonExistientMajor(self):
        # The major in this doesn't exist in the test database!
        getData = "?uni=exampleUni&outstate=true&dept=exampleDept&major=nonExistientMajor&aid="

        response = self.client.get(self.infoUrl+getData)

        # The status code should still be 200
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response['content-type'], 'application/json')

        data = json.loads(response.content)

        self.assertEqual(data["major"]["name"], self.DNE)


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
        
class MajorModelTest(TestCase):
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

