from django.db import models
from .rare_user import RareUser

class Post(models.Model):
    rare_user = models.ForeignKey(RareUser, related_name="posts", on_delete=models.CASCADE)
    # categories = models.ManyToManyField(Category, related_name="posts", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    publication_date = models.DateField()
    image_url = models.CharField(max_length=400)
    content = models.CharField(max_length=1000)
    approved = models.BooleanField(default=False)
    
    @property
    def rare_user_id(self):
        return self.rare_user.id
