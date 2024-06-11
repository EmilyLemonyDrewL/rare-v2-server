from django.db import models
from .rare_user import RareUser

class UserTypeChangeRequest(models.Model):
    action = models.CharField(max_length=50)
    admin_one_id = models.ForeignKey(RareUser, on_delete=models.CASCADE, related_name="admin_one")
    admin_two_id = models.ForeignKey(RareUser, on_delete=models.CASCADE, related_name="admin_two")
    modified_user_id = models.ForeignKey(RareUser, on_delete=models.CASCADE, related_name="modified_user")
