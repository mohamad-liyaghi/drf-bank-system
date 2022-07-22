from django.db import models
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
import random

class CardManager(models.Manager):
    '''
        Overriding create card function
    '''
    def create(self, request, password):
        user = request.user
        if not user.is_authenticated:
            raise ValueError("User must be authenticated")

        if not password:
            raise ValueError("Password field must not be empty")

        if user.cards.all().count() >= 5:
            raise  ValueError("Users are not allowed to have more than 5 cards")

        card = self.model(
            owner = user,
            number = random.randint(1111111111, 9999999999),
            cvv = random.randint(100, 9999),
            password= password,
            token= random.randint(111111111111, 999999999999999)
        )

        card.save()
        return card