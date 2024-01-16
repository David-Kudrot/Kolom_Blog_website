from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserAccountModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image=models.ImageField(upload_to="accounts/images")
    phone_no = models.CharField(max_length=15)
    
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name