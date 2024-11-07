import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin

# Create your models here.

class Post(models.Model):
    username = models.CharField(max_length=50)
    post_text = models.CharField(max_length=500)
    pub_date = models.DateTimeField("date published")
    likes = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.username}: {self.post_text}"
    
    
class Reply(models.Model):
    userpost = models.ForeignKey(Post, on_delete=models.CASCADE)
    username = models.CharField(max_length=50)
    reply_text = models.CharField(max_length=500)
    pub_date = models.DateTimeField("date published")
    likes = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.username}: {self.reply_text}"
    
    

# Imported from my research milestone for skeleton of file - Brandon 
