# MajorHelp/urls.py

from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls.converters import register_converter
from django.contrib.auth.views import LogoutView
from MajorHelp.views import main_views as main_views
from MajorHelp.views import calc as calc_views
#from MajorHelp.views.main_views import * # about,contact, SearchView, SchoolResultsView, DepartmentResultsView, LeaveReview
from MajorHelp.views.forms import CustomAuthenticationForm

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
    path("", main_views.HomeView.as_view(), name="home"),
    
    # Uni overview views urls
    path('UniversityOverview/<str:slug>/', main_views.UniversityOverviewView.as_view(), name='university-detail'),
    path('SubmitRating/<int:pk>/', main_views.SubmitRatingView.as_view(), name='submit-rating'),
    # Leave review for University
    path('create/review/<str:username>/', main_views.LeaveUniversityReview.as_view(), name="create_review"),
   
    # Adding login and signup views
    path('accounts/login/', main_views.LoginView.as_view(authentication_form=CustomAuthenticationForm), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/signup/', main_views.SignUpView.as_view(), name='signup'),
    path('accounts/activate/<str:token>/', main_views.activate_account, name='activate_account'),
    path('accounts/settings/', main_views.settings_view, name='settings'),
    path('accounts/check-email/', main_views.check_email_view, name='check_email'),

    # URLS for the Contact and About page
    path('about/', main_views.about, name='about'),
    path('contact/', main_views.contact, name='contact'),
    
    #urls for search and search results
    path('search/', main_views.SearchView.as_view(), name='search'),
    path('search/school/<str:query>/', main_views.SchoolResultsView.as_view(), name='school_results'),
    path('search/department/<str:query>/', main_views.DepartmentResultsView.as_view(), name='department_results'),
    path('search/major/<str:query>/', main_views.MajorResultsView.as_view(), name='major_results'),
    path('search/university-request/', main_views.UniversityRequestView.as_view(), name='university-request'),

    #urls for major overviews
    path('MajorOverview/<slashslug:slug>/', main_views.MajorOverviewView.as_view(), name='major-detail'),
    # Leave review for Major
    path('create/review/major/<str:username>/', main_views.LeaveMajorReview.as_view(), name='create_major_review'),
    

    # URLS for the Tuition Calculator
    path('calc/', calc_views.CalcView.as_view(), name='calc'),
    path("api/university_search/", calc_views.university_search, name="university_search"),
    path("api/aid/", calc_views.aid_list, name="aid_list"),
    path("api/majors/", calc_views.major_list, name="major_list"),
    path("api/calculate/", calc_views.calculate, name="calculate"),
    path("api/calcs/", calc_views.calc_list, name="calc_list"),
    path("api/save_calc/", calc_views.save_calc, name="save_calc"),

    # dicussions URLs
    path('discussion/', main_views.discussion_board, name='discussion_board'),
    path('discussion/categories/', main_views.DiscussionCategoryListView.as_view(), name='discussion_categories'),
    path('discussion/thread/<int:pk>/', main_views.discussion_detail, name='discussion_detail'),
    path('discussion/thread/<int:pk>/', main_views.DiscussionThreadDetailView.as_view(), name='discussion_detail'),
    path('discussion/new/', main_views.create_thread, name='create_thread'),
    path('discussion/thread/<int:pk>/delete/', main_views.delete_thread, name='delete_thread'),
    path('discussion/reply/<int:pk>/delete/', main_views.delete_reply, name='delete_reply'),
    path('discussion/my-posts/', main_views.my_discussions, name='my_discussions'),
    path('discussion/mine/', main_views.MyThreadsView.as_view(), name='my_threads'),
    path('discussion/category/<int:category_id>/', main_views.DiscussionThreadListView.as_view(), name='category_threads'),

    # major chat urls
    path('majorchat/', main_views.major_chat, name='major_chat'),

    #URLS for favorite page
    path('toggle-favorite/<str:object_type>/<int:object_id>/', main_views.toggle_favorite, name='toggle-favorite'),
    path('favorites/', main_views.favorites_list, name='favorites-list'),

    # majorhelp map url
    path('map/', main_views.college_map, name='college_map'),
    path('api/universities/mapdata/', main_views.university_map_data, name='university_map_data'),
    path('university/<int:pk>/submit-overall-rating/', main_views.SubmitOverallRatingView.as_view(), name='submit-overall-rating'),
    path('university/<int:pk>/delete-review/', main_views.DeleteReviewView.as_view(), name='delete-review'),

]