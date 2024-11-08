import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.db.models import Avg
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

# Model for university
class University(models.Model):
    name = models.TextField()
    aboutText = models.TextField()
    TotalUndergradStudents = models.IntegerField()
    TotalGradStudents = models.IntegerField()
    GraduationRate = models.DecimalField(max_digits=4, decimal_places=1)
    
    # Calculate the average rating for a given category
    def get_average_rating(self, category):
        average = self.ratings.filter(category=category).aggregate(Avg('rating'))['rating__avg']
        if average is not None:
            return round(float(average), 1)  # Convert to float and round to 1 decimal place
        return 0.0  # Default to 0.0 if no ratings are available

    def campus_rating(self):
        return self.get_average_rating('campus')

    def athletics_rating(self):
        return self.get_average_rating('athletics')

    def safety_rating(self):
        return self.get_average_rating('safety')

    def social_rating(self):
        return self.get_average_rating('social')

    def professor_rating(self):
        return self.get_average_rating('professor')

    def dorm_rating(self):
        return self.get_average_rating('dorm')

    def dining_rating(self):
        return self.get_average_rating('dining')
    
    def __str__(self):
        return f"{self.name}"
    
# instance of a rating for a university, uses foreign key to refrence that university    
class UniversityRating(models.Model):
    CATEGORY_CHOICES = [
        ('campus', 'Campus'),
        ('athletics', 'Athletics'),
        ('safety', 'Safety'),
        ('social', 'Social'),
        ('professor', 'Professor'),
        ('dorm', 'Dorm'),
        ('dining', 'Dining'),
    ]
    
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='ratings')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    rating = models.DecimalField(max_digits=2, decimal_places=1, validators=[MinValueValidator(1), MaxValueValidator(5)])

    # Ensure the rating is within the 1-5 range
    def save(self, *args, **kwargs):
        if self.rating < 1:
            self.rating = 1
        elif self.rating > 5:
            self.rating = 5
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.university.name} - {self.category}: {self.rating}"



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
    