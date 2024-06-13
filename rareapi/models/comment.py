from django.db import models
from .rare_user import RareUser
from .post import Post
from django.utils import timezone

class Comment(models.Model):

    author = models.ForeignKey(RareUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.CharField(max_length=140)
    created_on = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.content
