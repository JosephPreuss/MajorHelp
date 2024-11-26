from django.contrib import admin
from .models import UniversityReview, University, UniversityRating, Major, MajorReview

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
    
class MajorAdmin(admin.ModelAdmin):
    list_display = (
        'major_name',
        'university',
        'department',
        'in_state_min_tuition',
        'in_state_max_tuition',
        'out_of_state_min_tuition',
        'out_of_state_max_tuition',
    )
    list_filter = ('university', 'department')
    search_fields = ('major_name', 'major_description')  

# Registering models
admin.site.register(University, UniversityAdmin)
admin.site.register(UniversityRating, UniversityRatingAdmin)
admin.site.register(UniversityReview, UniversityReviewAdmin)
admin.site.register(Major, MajorAdmin)
admin.site.register(MajorReview, MajorReviewAdmin)