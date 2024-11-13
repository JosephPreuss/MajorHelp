from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.db.models import F
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.views import View
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.views.generic import *
from django.contrib import messages


from .models import *



# HomeView displays the homepage
class HomeView(TemplateView):
    template_name = "MajorHelp/HomePage.html"

#University overview page 
class UniversityOverviewView(DetailView):
    model = University
    template_name = "MajorHelp/UniOverviewPage.html"
    context_object_name = "university" 
    
    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       # Filter reviews related to the specific university
       context['latest_post_list'] = Review.objects.filter(university=self.object)
       return context
    
# View for submitting a rating to a specific catagory of a cartain university    
class SubmitRatingView(View):
    def post(self, request, pk):
        university = get_object_or_404(University, pk=pk)
        
        # Get the category and rating from the submitted form data
        category = request.POST.get('category')
        rating_value = int(request.POST.get('rating'))
        
        # Ensure the rating is between 1 and 5
        if category in ['campus', 'athletics', 'safety', 'social', 'professor', 'dorm', 'dining'] and 1 <= rating_value <= 5:
            UniversityRating.objects.create(
                university=university,
                category=category,  # Use the selected category
                rating=rating_value
            )
        else:
            messages.error(request, 'Invalid rating. Please select a value between 1 and 5.')

        return redirect('MajorHelp:university-detail', pk=pk)

class LeaveReview(View):
    def post(self, request, *args, **kwargs):
        university_id = kwargs.get("university_id")  # Get university ID from URL arguments
        post_text = request.POST.get("post_text")

        if post_text:
            # Create the review
            Review.objects.create(
                username=request.user.username,
                text=post_text,
                pub_date=timezone.now()
            )
            messages.success(request, "Your review has been submitted.")
            return redirect("MajorHelp:university-detail", pk=university_id)
        else:
            messages.error(request, "Failed to submit the review.")
            return redirect("MajorHelp:university-detail", pk=university_id)

class LeaveReview(View):
    def post(self, request, username):
        review_text = request.POST.get("review_text", "")
        if review_text:
            university_id = request.POST.get("university_id")  # Make sure university_id is passed in the form
            university = get_object_or_404(University, pk=university_id)
            Review.objects.create(
                username=request.user.username,
                review_text=review_text,
                university=university
            )
            # Redirect to the specific university's detail page
            return redirect("MajorHelp:university-detail", pk=university_id)
        return redirect("MajorHelp:university-detail", pk=university_id)
    
    
# Custom form for SignUp with 'Password' and 'Confirm password'
class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm password")

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password']

    # Customizing the validation message for the username field
    username = forms.CharField(
        max_length=150,
        help_text="",
        error_messages={
            'required': 'Please enter a username.',
            'max_length': 'Username should not exceed 150 characters.',
        }
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return confirm_password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Hash the password
        if commit:
            user.save()
        return user


# SignUpView for user registration
class SignUpView(View):
    def get(self, request):
        form = CustomUserCreationForm()  # Use the custom form here
        return render(request, 'registration/signup.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user
            return redirect('MajorHelp:login')  # Redirect to home page after successful signup
        return render(request, 'registration/signup.html', {'form': form})

def about(request):
    return render(request, 'About/about.html')
    
def contact(request):
    return render(request,'Contact/contact.html')

#the search function
class SearchView(View):
    def get(self, request):
        query = request.GET.get('query', '')
        filter_type = request.GET.get('filter', 'department')
        
        # If the query is empty, reload the search page without redirecting
        if not query:
            return render(request, 'search/search.html', {'query': query, 'filter_type': filter_type})
        
        # Redirect based on the filter type if query is provided
        if filter_type == 'school':
            return redirect('MajorHelp:school_results', query=query)
        elif filter_type == 'department':
            return redirect('MajorHelp:department_results', query=query)
        elif filter_type == 'major':
            return redirect('MajorHelp:major_results', query=query)
        
        # Default behavior (in case of other filter types)
        return render(request, 'search/search.html', {'query': query, 'filter_type': filter_type})

class SchoolResultsView(View):
    def get(self, request, query):
        # Placeholder for actual search logic (replace with database query if available)
        results = []  # Replace with real data, e.g., School.objects.filter(name__icontains=query)
        
        # Render the template with the search query and any results
        return render(request, 'search/school_results.html', {'query': query, 'results': results})
    
class DepartmentResultsView(View):
    def get(self, request, query):
        # Fetch all majors in the specified department
        majors = Major.objects.filter(department=query)
        
        # Group majors by school
        results = {}
        for major in majors:
            school_name = major.university.name  # Adjust based on your model relationships
            if school_name not in results:
                results[school_name] = []
            results[school_name].append(major)
        
        # Render the template with grouped results
        return render(request, 'search/department_results.html', {'query': query, 'results': results})
    
class MajorResultsView(View):
    def get(self, request, query):
        # Placeholder for actual search logic (replace with database query if available)
        results = []  # Replace with actual query, e.g., Major.objects.filter(name__icontains=query)
        
        # Render the major_results.html template with the search query and results
        return render(request, 'search/major_results.html', {'query': query, 'results': results})