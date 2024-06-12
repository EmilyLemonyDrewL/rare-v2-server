from django.db import models
from .rare_user import RareUser

class Subscription(models.Model):
    follower = models.ForeignKey(RareUser, on_delete=models.CASCADE, related_name='subscriptions_as_author')
    author = models.ForeignKey(RareUser, on_delete=models.CASCADE, related_name='subscriptions_as_follower')
    created_on = models.DateField(auto_now_add=True)
