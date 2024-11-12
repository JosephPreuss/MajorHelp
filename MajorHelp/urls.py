# MajorHelp/urls.py

from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from MajorHelp.views import about,contact

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
    path("<int:pk>/", views.PostView.as_view(), name="post"),
    path("like/post/<int:post_id>/", views.likePost, name="like_post"),
    path("like/reply/<int:reply_id>/", views.likeReply, name="like_reply"),
    path("create/post/<str:username>/", views.create_post, name="create_post"),
    path("create/reply/<str:username>/<int:post_id>/", views.create_reply, name="create_reply"),
    
    # URLS for the Contact and About page
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),

]