from django.contrib import admin
from .models import *

# Inline for displaying University Ratings in University admin
class UniversityRatingInline(admin.TabularInline):
    model = UniversityRating
    extra = 1

class UniversityAdmin(admin.ModelAdmin):
    inlines = [UniversityRatingInline]  # Display ratings inline

class UniversityRatingAdmin(admin.ModelAdmin):
    list_display = ('university', 'category', 'rating')
    list_filter = ('university', 'category')
    
class UniversityReviewAdmin(admin.ModelAdmin):
    list_display = ('username', 'university', 'review_text')
    list_filter = ('university',)
    
    fieldsets = (
        (None, {
            'fields': ('username', 'university', 'review_text', 'pub_date')
        }),
    )

    readonly_fields = ('pub_date',)
    
class MajorReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'university', 'review_text')
    list_filter = ('university',)
    
    fieldsets = (
        (None, {
            'fields': ('user', 'university', 'review_text', 'pub_date')
        }),
    )

    readonly_fields = ('pub_date',)

# Inline for managing Courses in Major admin
class CourseInline(admin.TabularInline):
    model = Course  # Use the Course model
    extra = 1  # Display one blank row for adding new courses

    # Ensure the inline references the ManyToMany relationship correctly
    fk_name = 'major'

# Admin configuration for Major
class MajorAdmin(admin.ModelAdmin):
    list_display = (
        'major_name',
        'university',
        'department',
        'in_state_min_tuition',
        'in_state_max_tuition',
        'out_of_state_min_tuition',
        'out_of_state_max_tuition',
        'grad_in_state_min_tuition',
        'grad_in_state_max_tuition',
        'grad_out_of_state_min_tuition',
        'grad_out_of_state_max_tuition',
    )
    list_filter = ('university', 'department')
    search_fields = ('major_name', 'major_description')
    inlines = [CourseInline]  # Include CourseInline in MajorAdmin

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role')
    list_filter = ('role',)

# Registering models
admin.site.register(University, UniversityAdmin)
admin.site.register(UniversityRating, UniversityRatingAdmin)
admin.site.register(UniversityReview, UniversityReviewAdmin)
admin.site.register(Major, MajorAdmin)
admin.site.register(MajorReview, MajorReviewAdmin)
admin.site.register(CustomUser, UserAdmin)
admin.site.register(FinancialAid)