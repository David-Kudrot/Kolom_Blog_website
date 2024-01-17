from django.db import models
from django.contrib.auth.models import User


USER_CATEGORIES = [
        ('admin', 'Admin'),
        ('author', 'Author'),
        ('reader', 'Reader'),
    ]


class UserAccountModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_category = models.CharField(max_length=10, choices=USER_CATEGORIES, null=True, blank=True)
    profile_picture = models.ImageField(upload_to="profile_picture/", null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.user_category}"
