from django.contrib import admin
from django.urls import include, path
from MajorHelp.views import about, contact, SearchView, SchoolResultsView, DepartmentResultsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("MajorHelp.urls", namespace="MajorHelp")),  # This removes the "MajorHelp" prefix from all URLs in MajorHelp
    path('accounts/', include('django.contrib.auth.urls')),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('search/', SearchView.as_view(), name='search'),
    path('search/school/<str:query>/', SchoolResultsView.as_view(), name='school_results'),
    path('search/department/<str:query>/', DepartmentResultsView.as_view(), name='department_results'),
]
