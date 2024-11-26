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
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model


def settings_view(request):
    return render(request, 'settings.html')  # Make sure you have a 'settings.html' template, or adjust accordingly

# HomeView displays the homepage
class HomeView(TemplateView):
    template_name = "MajorHelp/HomePage.html"

#University overview page 
class UniversityOverviewView(DetailView):
    model = University
    template_name = "MajorHelp/UniOverviewPage.html"
    context_object_name = "university"

    # Use slug as the lookup field
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_object(self):
        slug = self.kwargs['slug']
        return get_object_or_404(University, slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_post_list'] = UniversityReview.objects.filter(university=self.object)
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
            rating, created = UniversityRating.objects.update_or_create(
                university=university,
                category=category,  # Use the selected category
                user=request.user,
                defaults={'rating': rating_value}
            )
            if created:
                messages.success(request, 'Your rating has been submitted.')
            else:
                messages.success(request, 'Your rating has been updated.')
        else:
            messages.error(request, 'Invalid rating. Please select a value between 1 and 5.')

        return redirect('MajorHelp:university-detail', slug=university.slug)

class LeaveUniversityReview(View):
    def post(self, request, username):
        review_text = request.POST.get("review_text", "")
        if review_text:
            university_id = request.POST.get("university_id")
            university = get_object_or_404(University, pk=university_id)
            UniversityReview.objects.create(
                username=request.user.username,
                review_text=review_text,
                university=university
            )
            messages.success(request, 'Your review has been submitted successfully!')
        else:
            messages.error(request, 'Review text cannot be empty.')

        return redirect('MajorHelp:university-detail', slug=university.slug)

    
    
# Custom form for SignUp with 'Password' and 'Confirm password'
class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your Password'}), label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your Password'}), label="Confirm password")
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Enter your Email'}))
    role = forms.ChoiceField(
        choices=[('', 'Select a role')] + [choice for choice in CustomUser.ROLE_CHOICES if choice[0] != 'admin'],
        widget=forms.Select()
    )
    
    class Meta:
        model = get_user_model()  # Use the custom user model dynamically
        fields = ['username', 'email', 'password', 'confirm_password', 'role']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter your Username'}), #placeholder text in username box
        }
        labels = {
            'username': 'Username', # change the labe of the username entry box
        }
        help_texts = {
            'username': '', # help text by username entry box if we want to add
        }

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return confirm_password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = self.cleaned_data['role']
        user.set_password(self.cleaned_data["password"])  # Hash the password
        if commit:
            user.save()
        return user


# SignUpView for user registration
class SignUpView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'registration/signup.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user
            login(request, user)  # Log the user in immediately after signup
            messages.success(request, 'Account created successfully.')
            return redirect('MajorHelp:home')  # Redirect to home page after successful signup
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
        # Fetch universities matching the query (case-insensitive, partial matches)
        universities = University.objects.filter(name__icontains=query)
        
        results = {}
        for university in universities:
            departments = {}
            # Group majors by department
            for major in university.majors.all():
                if major.department not in departments:
                    departments[major.department] = []
                departments[major.department].append(major)
            
            # Add university details and grouped departments to results
            results[university] = {
                'location': university.location,
                'type': 'Public' if university.is_public else 'Private',
                'departments': departments
            }
        
        return render(request, 'search/school_results.html', {'query': query, 'results': results})
class DepartmentResultsView(View):
    def get(self, request, query):
        # Fetch all majors in the specified department
        majors = Major.objects.filter(department__icontains=query)

        # Group majors by university and department
        results = {}
        for major in majors:
            university = major.university
            if university not in results:
                results[university] = {
                    'location': university.location,
                    'type': 'Public' if university.is_public else 'Private',
                    'departments': {}
                }
            
            if major.department not in results[university]['departments']:
                results[university]['departments'][major.department] = []
            
            results[university]['departments'][major.department].append(major)

        # Render the results page with grouped data
        return render(request, 'search/department_results.html', {'query': query, 'results': results})
class MajorResultsView(View):
    def get(self, request, query):

        # Fetch majors that match the query (case-insensitive and partial matches)
        majors = Major.objects.filter(major_name__icontains=query)

        # Group majors by university and department
        results = {}
        for major in majors:
            university = major.university
            if university not in results:
                results[university] = {
                    'location': university.location,
                    'type': 'Public' if university.is_public else 'Private',
                    'departments': {}
                }
            
            if major.department not in results[university]['departments']:
                results[university]['departments'][major.department] = []
            
            results[university]['departments'][major.department].append(major)

        # Render the template with grouped data
        return render(request, 'search/major_results.html', {'query': query, 'results': results})
    
#major overview view
class MajorOverviewView(DetailView):
    model = Major
    template_name = "major/MajorOverviewPage.html"
    context_object_name = "major"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch all reviews related to the major
        context['reviews'] = self.object.major_reviews.all()
        print(f"Reviews: {context['reviews']}")  # Debug: print reviews
        
        return context


class CalcView(View):
    def get(self, request):
        return render(request, 'calc/calc.html')

# LeaveMajorReview View - Exclusive for leaving reviews for a major at a specific school

@login_required
def LeaveMajorReview(request, slug):
    # Fetch the major based on the slug
    major = Major.objects.get(slug=slug)

    # Check if the form is submitted via POST
    if request.method == 'POST':
        # Get the review text from the form
        review_text = request.POST.get('review_text')

        # Create and save the review using the MajorReview model
        MajorReview.objects.create(
            major=major,
            user=request.user,  # Use request.user which is a User object
            review_text=review_text,
            university=major.university  # Link the university associated with the major
        )

        # Redirect to the same major overview page after the review is saved
    return redirect('MajorHelp:major-detail', slug=slug)

    # If the request is not a POST, render the review form (this is optional)
    return render(request, 'leave_review.html', {'major': major})