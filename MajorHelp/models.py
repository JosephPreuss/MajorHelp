import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin

# Create your models here.

# Model for university
class University(models.Model):
    name = models.TextField()
    aboutText = models.TextField()
    CampusRating = models.DecimalField(max_digits=2, decimal_places=1)
    AthleticsRating = models.DecimalField(max_digits=2, decimal_places=1)
    SafteyRating = models.DecimalField(max_digits=2, decimal_places=1)
    SocialRating = models.DecimalField(max_digits=2, decimal_places=1)
    ProffesorRating = models.DecimalField(max_digits=2, decimal_places=1)
    DormRating = models.DecimalField(max_digits=2, decimal_places=1)
    DiningRating = models.DecimalField(max_digits=2, decimal_places=1)
    GraduationRate = models.DecimalField(max_digits=4, decimal_places=1)
    TotalUndergradStudents = models.IntegerField()
    TotalGradStudents = models.IntegerField()
    def __str__(self):
        return f"{self.name}"



# Imported from my research milestone for skeleton of file - Brandon 
# Model for a post
class Post(models.Model):
    username = models.CharField(max_length=50)
    post_text = models.CharField(max_length=500)
    pub_date = models.DateTimeField("date published")
    likes = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.username}: {self.post_text}"
    
# Model for a reply to a post   
class Reply(models.Model):
    userpost = models.ForeignKey(Post, on_delete=models.CASCADE)
    username = models.CharField(max_length=50)
    reply_text = models.CharField(max_length=500)
    pub_date = models.DateTimeField("date published")
    likes = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.username}: {self.reply_text}"
    