from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import *
from .models import DiscussionCategory, DiscussionThread, ThreadReply
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.urls import path
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.utils.html import format_html

#
admin.site.register(DiscussionCategory)
admin.site.register(DiscussionThread)
admin.site.register(ThreadReply)

# Get the custom user model
CustomUser = get_user_model()

# Inline for displaying University Ratings in University admin
class UniversityRatingInline(admin.TabularInline):
    model = UniversityRating
    extra = 1

class UniversityAdmin(admin.ModelAdmin):
    inlines = [UniversityRatingInline]  # Display ratings inline
    search_fields = ['name'] 

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

class UniversityRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'request_text', 'submitted_at')
    list_filter = ('submitted_at',)
    search_fields = ('request_text', 'user__username')

# styled to display the user, what they favorited and when it was made
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_favorite', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = (
        'user__username',
        'university__name',
        'major__major_name',
        'major__university__name'
    )
    date_hierarchy = 'created_at'
    raw_id_fields = ('user', 'university', 'major')

    def display_favorite(self, obj):
        if obj.university:
            return f"University: {obj.university.name}"
        return f"Major: {obj.major.major_name} ({obj.major.university.name})"
    display_favorite.short_description = 'Favorite Item'

class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role', 'clear_saved_calcs_link')
    list_filter = ('role',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'password1', 'password2'),
        }),
    )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('clear-saved-calcs/<int:user_id>/', self.admin_site.admin_view(self.clear_saved_calcs), name='clear_saved_calcs'),
        ]
        return custom_urls + urls

    def clear_saved_calcs_link(self, obj):
        return format_html(
            '<a class="button" href="{}">Clear Saved Calcs</a>',
            f'clear-saved-calcs/{obj.id}'
        )
    clear_saved_calcs_link.short_description = 'Saved Calcs'

    def clear_saved_calcs(self, request, user_id):
        user = CustomUser.objects.get(id=user_id)
        user.savedCalcs = {}
        user.save()
        self.message_user(request, f"All saved calculators cleared for {user.username}.", messages.SUCCESS)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# Registering models
admin.site.register(University, UniversityAdmin)
admin.site.register(UniversityRating, UniversityRatingAdmin)
admin.site.register(UniversityReview, UniversityReviewAdmin)
admin.site.register(Major, MajorAdmin)
admin.site.register(MajorReview, MajorReviewAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(FinancialAid)
admin.site.register(UniversityRequest, UniversityRequestAdmin)
admin.site.register(Course)
admin.site.register(Favorite, FavoriteAdmin)  # New Favorite admin