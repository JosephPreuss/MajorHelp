# MajorHelp/urls.py

from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls.converters import register_converter
from . import views
from django.contrib.auth.views import LogoutView
from MajorHelp.views import * # about,contact, SearchView, SchoolResultsView, DepartmentResultsView, LeaveReview
from .forms import CustomAuthenticationForm
from MajorHelp.views import (
    DiscussionCategoryListView,
    DiscussionThreadListView,
    DiscussionThreadDetailView,
)
from MajorHelp.views import DiscussionThreadListView

app_name = "MajorHelp"

#so slashes can be used for slugs
class SlashSlugConverter:
    regex = r'[a-zA-Z0-9_-]+(/[a-zA-Z0-9_-]+)?'
    
    def to_python(self, value):
        return value
    
    def to_url(self, value):
        return value
register_converter(SlashSlugConverter, 'slashslug')


urlpatterns = [
    # Path for Home Page
    path("", views.HomeView.as_view(), name="home"),
    
    # Uni overview views urls
    path('UniversityOverview/<str:slug>/', views.UniversityOverviewView.as_view(), name='university-detail'),
    path('SubmitRating/<int:pk>/', views.SubmitRatingView.as_view(), name='submit-rating'),
    # Leave review for University
    path('create/review/<str:username>/', LeaveUniversityReview.as_view(), name="create_review"),
   
    # Adding login and signup views
    path('accounts/login/', LoginView.as_view(authentication_form=CustomAuthenticationForm), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/signup/', views.SignUpView.as_view(), name='signup'),
    path('accounts/activate/<str:token>/', activate_account, name='activate_account'),
    path('accounts/settings/', views.settings_view, name='settings'),
    path('accounts/check-email/', views.check_email_view, name='check_email'),

    # URLS for the Contact and About page
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    
    #urls for search and search results
    path('search/', SearchView.as_view(), name='search'),
    path('search/school/<str:query>/', SchoolResultsView.as_view(), name='school_results'),
    path('search/department/<str:query>/', DepartmentResultsView.as_view(), name='department_results'),
    path('search/major/<str:query>/', views.MajorResultsView.as_view(), name='major_results'),
    path('search/university-request/', UniversityRequestView.as_view(), name='university-request'),

    #urls for major overviews
    path('MajorOverview/<slashslug:slug>/', views.MajorOverviewView.as_view(), name='major-detail'),
    # Leave review for Major
    path('create/review/major/<str:username>/', LeaveMajorReview.as_view(), name='create_major_review'),
    

    # URLS for the Tuition Calculator
    path('calc/', CalcView.as_view(), name='calc'),
    path("api/university_search/", university_search, name="university_search"),
    path("api/aid/", aid_list, name="aid_list"),
    path("api/majors/", major_list, name="major_list"),
    path("api/calculate/", calculate, name="calculate"),
    path("api/calcs/", calc_list, name="calc_list"),
    path("api/save_calc/", save_calc, name="save_calc"),

    # dicussions URLs
    path('discussion/', views.discussion_board, name='discussion_board'),
    path('discussion/categories/', DiscussionCategoryListView.as_view(), name='discussion_categories'),
    path('discussion/thread/<int:pk>/', views.discussion_detail, name='discussion_detail'),
    path('discussion/thread/<int:pk>/', DiscussionThreadDetailView.as_view(), name='discussion_detail'),
    path('discussion/new/', views.create_thread, name='create_thread'),
    path('discussion/thread/<int:pk>/delete/', views.delete_thread, name='delete_thread'),
    path('discussion/reply/<int:pk>/delete/', views.delete_reply, name='delete_reply'),
    path('discussion/my-posts/', views.my_discussions, name='my_discussions'),
    path('discussion/mine/', views.MyThreadsView.as_view(), name='my_threads'),
    path('discussion/category/<int:category_id>/', DiscussionThreadListView.as_view(), name='category_threads'),

    # major chat urls
    path('majorchat/', views.major_chat, name='major_chat'),

    #URLS for favorite page
    path('toggle-favorite/<str:object_type>/<int:object_id>/', views.toggle_favorite, name='toggle-favorite'),
    path('favorites/', favorites_list, name='favorites-list'),

    # majorhelp map url
    path('map/', views.college_map, name='college_map'),
    path('api/universities/mapdata/', views.university_map_data, name='university_map_data'),
]