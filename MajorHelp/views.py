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
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm 
from django import forms
from django.contrib.auth.models import User

from django.views.generic import *


from .models import Post, Reply, University


from django.views.generic import *
from .forms import CustomUserCreationForm 
from django import forms
from django.contrib.auth.models import User
from .models import Post, Reply, University
from .models import Post, Reply


# HomeView displays a list of posts on the homepage
class HomeView(TemplateView):
    template_name = "MajorHelp/HomePage.html"
    
class UniversityOverviewView(DetailView):
    model = University
    template_name = "MajorHelp/UniOverviewPage.html"
    context_object_name = "university"

# EVERYTHING BELOW HERE WAS IMPORTED FROM MY RESEARCH APP
# Should keep because we can use these for replies and posts

# add LoginRequiredMixin parameter when ready
# PostView displays the details of a single post
class PostView(LoginRequiredMixin, generic.DetailView):
    model = Post
    template_name = "MajorHelp/detail.html"
    login_url = "/accounts/login/"
    def get_queryset(self):
        return Post.objects.filter(pub_date__lte=timezone.now())
        
# Function to handle liking a post, increments count for a post
def likePost(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=post_id)
        post.likes = F('likes') + 1
        post.save()
        # Reload the instance to get the updated like count after the increment
        post.refresh_from_db()
        return JsonResponse({'likes': post.likes})

    return JsonResponse({'error': 'Invalid request'}, status=400)   

# Function to handle liking a reply
def likeReply(request, reply_id):
    if request.method == "POST":
        reply = get_object_or_404(Reply, pk=reply_id)        
        reply.likes = F('likes') + 1
        reply.save()
        # Reload the instance to get the updated like count after the increment
        reply.refresh_from_db()
        return JsonResponse({'likes': reply.likes})

    return JsonResponse({'error': 'Invalid request'}, status=400)

# Function to create a new post
# Only logged-in users can create a post
def create_post(request, username):
    if request.method == "POST":
        post_text = request.POST.get("post_text", "")
        pub_date = timezone.now()

        if post_text:
            # Use request.user.username instead of the username argument to ensure consistency
            Post.objects.create(username=request.user.username, post_text=post_text, pub_date=pub_date)
            return redirect("MajorHelp:home")

    return redirect("MajorHelp:home")

# Function to create a new reply associated with a specific post
# Only logged-in users can create a reply
def create_reply(request, username, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=post_id)
        reply_text = request.POST.get("reply_text", "")
        pub_date = timezone.now()

        if reply_text:
            Reply.objects.create(userpost=post, username=request.user.username, reply_text=reply_text, pub_date=pub_date)
            # Redirect to the post detail page after creating a reply
            return redirect("MajorHelp:post", pk=post_id)

    # If something goes wrong, redirect back to the post detail page
    return redirect("MajorHelp:post", pk=post_id)

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