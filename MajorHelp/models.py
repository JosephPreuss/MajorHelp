import datetime

from django.db import models
from django.forms import ValidationError
from django.utils import timezone
from django.contrib import admin
from django.db.models import Avg
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

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

    # Automatically populated slug
    slug = models.SlugField(default="", editable=False, null=False, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:  # Only generate slug if it's not already set
            # Remove spaces and create a slug
            self.slug = slugify(self.name).replace('-', '')
        super().save(*args, **kwargs)

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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='university_ratings')

    # Ensure one rating per category per user
    class Meta:
        unique_together = ('university', 'category', 'user')

    # Ensure the rating is within the 1-5 range
    def save(self, *args, **kwargs):
        if self.rating < 1:
            self.rating = 1
        elif self.rating > 5:
            self.rating = 5
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.university.name} - {self.category}: {self.rating}"

# Model for a uni review
class UniversityReview(models.Model):
    username = models.CharField(max_length=50)
    review_text = models.CharField(max_length=500)
    pub_date = models.DateTimeField(auto_now_add=True)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='university_review')
    
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

    university = models.ForeignKey(
        University,
        on_delete=models.CASCADE,
        related_name="majors"
    )
    major_name = models.CharField(max_length=255)
    major_description = models.TextField(blank=True)  # Add this line
    slug = models.SlugField(default="", editable=False, null=False, unique=True)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    in_state_min_tuition = models.IntegerField(
        validators=[MinValueValidator(0)],
        default=0,
    )
    in_state_max_tuition = models.IntegerField(
        validators=[MinValueValidator(0)],
        default=0,
    )
    out_of_state_min_tuition = models.IntegerField(
        validators=[MinValueValidator(0)],
        default=0,
    )
    out_of_state_max_tuition = models.IntegerField(
        validators=[MinValueValidator(0)],
        default=0,
    )

    def clean(self):
        if self.in_state_max_tuition < self.in_state_min_tuition:
            raise ValidationError("In-state max tuition cannot be less than in-state min tuition.")
        if self.out_of_state_max_tuition < self.out_of_state_min_tuition:
            raise ValidationError("Out-of-state max tuition cannot be less than out-of-state min tuition.")

    def save(self, *args, **kwargs):
        if not self.slug:
            university_slug = slugify(self.university.name).replace('-', '')
            major_slug = slugify(self.major_name).replace('-', '')
            self.slug = f"{university_slug}/{major_slug}"
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.major_name} at {self.university.name} "
            f"(In-state: ${self.in_state_min_tuition} - ${self.in_state_max_tuition}, "
            f"Out-of-state: ${self.out_of_state_min_tuition} - ${self.out_of_state_max_tuition})"
        )
def get_default_user():
    return User.objects.first().id

class MajorReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=get_default_user)
    review_text = models.TextField(max_length=500)
    pub_date = models.DateTimeField(auto_now_add=True)
    major = models.ForeignKey('Major', on_delete=models.CASCADE, related_name='major_reviews')
    university = models.ForeignKey('University', on_delete=models.CASCADE, default=1)  # Assuming 1 is a valid University ID

    def __str__(self):
        return f"{self.user.username}: {self.review_text}"
