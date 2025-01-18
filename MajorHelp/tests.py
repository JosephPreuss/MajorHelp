from django.test import TestCase

from django.test import Client

from django.urls import reverse

from .models import University, Major


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
        
