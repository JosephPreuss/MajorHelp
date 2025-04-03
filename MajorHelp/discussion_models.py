from django.db import models
from django.conf import settings

class DiscussionCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class DiscussionThread(models.Model):
    category = models.ForeignKey(DiscussionCategory, on_delete=models.CASCADE, related_name='threads')
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_pinned = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class ThreadReply(models.Model):
    thread = models.ForeignKey(DiscussionThread, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Reply by {self.author} on {self.thread}'
