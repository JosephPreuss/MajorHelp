# MajorHelp/urls.py

from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from MajorHelp.views import about,contact, SearchView, SchoolResultsView, DepartmentResultsView, LeaveReview

app_name = "MajorHelp"

urlpatterns = [
    # Path for Home Page
    path("", views.HomeView.as_view(), name="home"),
    
    # Uni overview views urls
    path('UniversityOverview/<int:pk>/', views.UniversityOverviewView.as_view(), name='university-detail'),
    path('SubmitRating/<int:pk>/', views.SubmitRatingView.as_view(), name='submit-rating'),
    
    # Adding login and signup views
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),  # Login view
    path('accounts/signup/', views.SignUpView.as_view(), name='signup'),  # Custom signup view
    
    
    # URLs for my research milestone could maybe use them later
    path("create/review/<str:username>/", LeaveReview.as_view(), name="create_review"),
    
    # URLS for the Contact and About page
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    
    path('search/', views.SearchView.as_view(), name='search'),
    path('search/school/<str:query>/', views.SchoolResultsView.as_view(), name='school_results'),
    path('search/department/<str:query>/', views.DepartmentResultsView.as_view(), name='department_results'),
    path('search/major/<str:query>/', views.MajorResultsView.as_view(), name='major_results'),

]