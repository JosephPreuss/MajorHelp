from django.contrib import admin

from .models import Post, Reply, University, UniversityRating
# Imported from my research milestone for skeleton of file - Brandon 

class ReplyInline(admin.TabularInline): 
    model = Reply
    extra = 3


admin.site.register(University)
admin.site.register(UniversityRating)
