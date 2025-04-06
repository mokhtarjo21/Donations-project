from django.db import models
from django.contrib.auth.models import AbstractUser
class User(AbstractUser):
    # id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.EmailField(unique=True) 
    password = models.CharField(max_length=50)
    facebook_acount = models.CharField(max_length=50, null=True,blank=True)
    Birthdate = models.DateTimeField(null=True, blank=True)
    phone = models.CharField(max_length=50)
    active_email = models.BooleanField(default=False)
    picture = models.ImageField(upload_to='users/', default='default.jpg')

    def __str__(self):
        return self.fname
    def save(self, *args, **kwargs):
        # Set username to email if not provided
        if not self.username:
            self.username = self.email
            
        # Use first_name and last_name instead of fname/lname
        if hasattr(self, 'fname'):
            self.first_name = self.fname
        if hasattr(self, 'lname'):
            self.last_name = self.lname
            
        super().save(*args, **kwargs)


class User_active(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.CharField(max_length=50)
    time_send = models.DateTimeField(auto_now_add=True)
    
# Create your models here.``