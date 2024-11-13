from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Model for university
class University(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)  # City and State
    is_public = models.BooleanField(default=True, help_text="Check if the university is public; leave unchecked for private")
    aboutText = models.TextField()
    TotalUndergradStudents = models.IntegerField()
    TotalGradStudents = models.IntegerField()
    GraduationRate = models.DecimalField(max_digits=4, decimal_places=1)
    
    # Calculate the average rating for a given category
    def get_average_rating(self, category):
        average = self.ratings.filter(category=category).aggregate(Avg('rating'))['rating__avg']
        return round(float(average), 1) if average is not None else 0.0

    def __str__(self):
        return f"{self.name} ({'Public' if self.is_public else 'Private'}) - {self.location}"


# Model for a rating of a university
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

    def __str__(self):
        return f"{self.university.name} - {self.category}: {self.rating}"


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


# Model for a major offered at a university
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
        return f"{self.name} at {self.university.name}"