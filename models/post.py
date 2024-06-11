from django.db import models
from .user import User
from .category import Category

class Post(models.Model):
    rare_user_id = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    category_id = models.ManyToManyField(Category, related_name="posts", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    publication_date = models.DateField()
    image_url = models.ImageField()
    content = models.CharField(max_length=1000)
    approved = models.BooleanField(default=False)
