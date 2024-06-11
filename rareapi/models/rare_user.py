from django.db import models

class RareUser(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    bio = models.CharField(max_length=400)
    profile_image_url = models.CharField(max_length=400)
    email = models.CharField(max_length=200)
    created_on = models.DateField()
    active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    uid = models.CharField(max_length=100)