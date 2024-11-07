from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "MajorHelp"

urlpatterns = [
    # Your existing paths
    path("", views.HomeView.as_view(), name="home"),
    path("<int:pk>/", views.PostView.as_view(), name="post"),
    path("like/post/<int:post_id>/", views.likePost, name="like_post"),
    path("like/reply/<int:reply_id>/", views.likeReply, name="like_reply"),
    path("create/post/<str:username>/", views.create_post, name="create_post"),
    path("create/reply/<str:username>/<int:post_id>/", views.create_reply, name="create_reply"),

    # Adding login and signup views
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),  # Login view
    path('accounts/signup/', views.SignUpView.as_view(), name='signup'),  # Custom signup view
]
