from django.db import models
from django.contrib.auth.models import AbstractUser
from version.v1.managers import CardManager, UserManager

class User(AbstractUser):
    username = None
    full_name = models.CharField(max_length=70)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["full_name"]
    objects = UserManager()

class Card(models.Model):
    owner = models.ForeignKey(User,null=True, on_delete=models.CASCADE, related_name="cards")
    number = models.BigIntegerField(unique=True)
    cvv = models.PositiveIntegerField(unique=True)
    balance = models.PositiveIntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=8)
    token = models.CharField(unique=True, max_length=15)

    objects = CardManager()

    def __str__(self):
        return  str(self.number)
