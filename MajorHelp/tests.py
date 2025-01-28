from django.test import TestCase

from django.test import Client

from django.urls import reverse

from .models import *


# Create your tests here.

class CalcTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        exampleUni = University.objects.create(name="exampleUni")
        Major.objects.create(major_name="exampleMajor", slug="exampleMajor", university=exampleUni)




    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.url = "MajorHelp:calc"


    def testCalcReturnsHtmlPageAfterNoGetRequest(self):
        """
        The calculator should only return a json file if a get request is fully
        filled out to the server, otherwise it will return an html page.
        """

        response = self.client.get(reverse(self.url))
        
        # check status code
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response['content-type'], 'text/html; charset=utf-8')

    def testCalcReturnsHtmlPageAfterPartialGetRequest(self):
        """
        "Partial" is defined here as some get entries being null. While some
        entries are already predefined with defaults, most are not.
        """

        getData = "?uni=exampleUni"

        response = self.client.get(reverse(self.url)+getData)

        # check status code
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response['content-type'], 'text/html; charset=utf-8')

    def testCalcReturnsHtmlPageAfterFullGetRequest(self):
        """
        "Full" is defined here as all entries being non-null.

        Note that empty entries are still considered valid.
        """
        
        getData = "?uni=exampleUni&outstate=true&dept=exampleDept&major=exampleMajor&aid="

        response = self.client.get(reverse(self.url)+getData)

        # check status code
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response['content-type'], 'application/json')


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