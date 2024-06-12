from django.db import models
from .rare_user import RareUser
from .categories import Category
from .tag import Tag

class Post(models.Model):
    rare_user = models.ForeignKey(RareUser, on_delete=models.CASCADE, related_name="post",)
    categories = models.ManyToManyField(Category, related_name='posts')
    tags = models.ManyToManyField(Tag, through='PostTag', related_name="posts")
    title = models.CharField(max_length=100)
    publication_date = models.DateField()
    image_url = models.CharField(max_length=400)
    content = models.CharField(max_length=1000)
    approved = models.BooleanField(default=False)
    
    @property
    def rare_user_id(self):
        return self.rare_user.id
