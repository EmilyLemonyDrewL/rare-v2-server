from django.db import models
from .rare_user import RareUser

class UserTypeChangeRequest(models.Model):
    ACTION_CHOICES = (
        ('promotion', 'Promotion'),
        ('demotion', 'Demotion'),
    )
    action = models.CharField(max_length=10, choices=ACTION_CHOICES, default='promotion')
    admin_one_id = models.ForeignKey(RareUser, on_delete=models.CASCADE, related_name="admin_one", null=True, blank=True)
    admin_two_id = models.ForeignKey(RareUser, on_delete=models.CASCADE, related_name="admin_two", null=True, blank=True)
    modified_user_id = models.ForeignKey(RareUser, on_delete=models.CASCADE, related_name="modified_user")
