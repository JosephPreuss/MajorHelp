from django.contrib import admin
from django.urls import include, path
from MajorHelp.views import about, contact, SearchView, SchoolResultsView, DepartmentResultsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("MajorHelp.urls", namespace="MajorHelp")),  # This removes the "MajorHelp" prefix from all URLs in MajorHelp
    path('accounts/', include('django.contrib.auth.urls')),
    
]
