from django.db import models
from .rare_user import RareUser

class Subscription(models.Model):
    follower = models.ForeignKey(RareUser, on_delete=models.CASCADE, related_name="subscriptions")
    author = models.ForeignKey(RareUser, on_delete=models.CASCADE, related_name="subscriptions")
    created_on = models.DateField(auto_now_add=True)
    ended_on = models.DateField()
