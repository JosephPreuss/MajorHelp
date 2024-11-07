from django.contrib import admin

from .models import Post, Reply
# Imported from my research milestone for skeleton of file - Brandon 

class ReplyInline(admin.TabularInline): 
    model = Reply
    extra = 3

class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["username","post_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ReplyInline]
    list_display = ["post_text", "pub_date"]
    list_filter = ["pub_date"]
    search_fields = ["post_text"]

admin.site.register(Post, PostAdmin)