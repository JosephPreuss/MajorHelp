from django.contrib import admin
from django.urls import path
from django.urls import include
from django.contrib.auth import views as auth_views

from . import views

#imported from my research milestone as a example since we need file anyway -Brandon

app_name = "MajorHelp"
urlpatterns = [    
    path("", views.HomeView.as_view(), name="home"),
    path("<int:pk>/", views.PostView.as_view(), name="post"),
    path("like/post/<int:post_id>/", views.likePost, name="like_post"),
    path("like/reply/<int:reply_id>/", views.likeReply, name="like_reply"),
    path("create/post/<str:username>/", views.create_post, name="create_post"),
    path("create/reply/<str:username>/<int:post_id>/", views.create_reply, name="create_reply"),
]