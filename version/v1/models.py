from django.db import models
from django.contrib.auth.models import User
from version.v1.managers import CardManager


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
