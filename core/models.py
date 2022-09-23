from django.db import models
from django.contrib.auth.models import AbstractUser
from core.managers import CardManager, UserManager, TransactionManager


class User(AbstractUser):
    '''Custom User Model'''

    username = None
    full_name = models.CharField(max_length=70)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["full_name"]
    objects = UserManager()

    def __str__(self):
        return self.email


class Card(models.Model):
    '''Card model'''
    owner = models.ForeignKey(User,null=True, on_delete=models.CASCADE,
                              related_name="cards")

    number = models.BigIntegerField(unique=True)
    cvv = models.PositiveIntegerField(unique=True)
    balance = models.PositiveIntegerField(default=0)
    password = models.CharField(max_length=8)
    token = models.CharField(unique=True, max_length=15)

    date_created = models.DateTimeField(auto_now_add=True)

    objects = CardManager()

    def __str__(self):
        return  str(self.number)



class Transaction(models.Model):
    '''Transaction Model'''

    code = models.CharField(max_length=13, unique=True)
    from_card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="transactions")
    to_card = models.ForeignKey(Card, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)

    objects= TransactionManager()

    def __str__(self):
        return str(self.code)
