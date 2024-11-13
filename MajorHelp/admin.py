from django.contrib import admin
from .models import Post, Reply, University, UniversityRating, Major

# Inline for displaying University Ratings in University admin
class UniversityRatingInline(admin.TabularInline):
    model = UniversityRating
    extra = 1

class UniversityAdmin(admin.ModelAdmin):
    inlines = [UniversityRatingInline]  # Display ratings inline

class UniversityRatingAdmin(admin.ModelAdmin):
    list_display = ('university', 'category', 'rating')
    list_filter = ('university', 'category')

class MajorAdmin(admin.ModelAdmin):
    list_display = ('major_name', 'university', 'department', 'in_state_tuition', 'out_of_state_tuition')
    list_filter = ('university', 'department')
    search_fields = ('major_name',)

# Registering models
admin.site.register(University, UniversityAdmin)
admin.site.register(UniversityRating, UniversityRatingAdmin)
admin.site.register(Major, MajorAdmin)
