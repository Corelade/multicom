from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

    def __str__(self):
        return self.username

class Business(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='images/', blank=True)

    def __str__(self):
        return self.name
    
class BusinessGoods(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    price = models.IntegerField()
    image = models.ImageField(upload_to='images/', blank=True)
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.item_name