import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.db.models import Avg
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

# Model for university
class University(models.Model):
    name = models.TextField()
    location = models.CharField(max_length=255)  # City and State
    is_public = models.BooleanField(default=True, help_text="Check if the university is public; leave unchecked for private")
    aboutText = models.TextField()
    TotalUndergradStudents = models.IntegerField()
    TotalGradStudents = models.IntegerField()
    GraduationRate = models.DecimalField(max_digits=4, decimal_places=1)
    
    slug = models.SlugField(default="", null=False, unique=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
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
        return self.name
    
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
class Review(models.Model):
    username = models.CharField(max_length=50)
    review_text = models.CharField(max_length=500)
    pub_date = models.DateTimeField(auto_now_add=True)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='review')
    
    def __str__(self):
        return f"{self.username}: {self.review_text}"
    
class Major(models.Model):
    DEPARTMENT_CHOICES = [
        ('Humanities and Social Sciences', 'Humanities and Social Sciences'),
        ('Natural Sciences and Mathematics', 'Natural Sciences and Mathematics'),
        ('Business and Economics', 'Business and Economics'),
        ('Education', 'Education'),
        ('Engineering and Technology', 'Engineering and Technology'),
        ('Health Sciences', 'Health Sciences'),
        ('Arts and Design', 'Arts and Design'),
        ('Agriculture and Environmental Studies', 'Agriculture and Environmental Studies'),
        ('Communication and Media', 'Communication and Media'),
        ('Law and Criminal Justice', 'Law and Criminal Justice'),
    ]

    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name="majors")  # Link to University
    major_name = models.CharField(max_length=255)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    in_state_tuition = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    out_of_state_tuition = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.major_name} at {self.university.name}"
    