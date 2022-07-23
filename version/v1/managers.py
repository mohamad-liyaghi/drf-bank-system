from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.shortcuts import get_object_or_404
import random

class UserManager(BaseUserManager):
    '''
        Manager for creating new user
    '''
    def create_user(self, full_name, email, password):

        if not full_name:
            raise ValueError("Users must have full name!")

        if not email:
            raise ValueError("Users must have Email")


        user = self.model(
            email= email, full_name= full_name
        )
        user.set_password(password)
        user.save(using= self._db)
        return user


    def create_superuser(self, full_name, email, password):
        user = self.create_user(full_name, email,  password)
        user.is_superuser= True
        user.is_staff= True
        user.save(using=self._db)
        return user


class CardManager(models.Manager):
    '''
        Overriding create card function
    '''
    def create(self, owner, password):

        if not owner:
            raise ValueError("Owner is required")

        if not password:
            raise ValueError("Password field must not be empty")

        if owner.cards.all().count() >= 5:
            raise  ValueError("Users are not allowed to have more than 5 cards")

        card = self.model(
            owner = owner,
            number = random.randint(1111111111, 9999999999),
            cvv = random.randint(100, 9999),
            password= password,
            token= random.randint(111111111111, 999999999999999)
        )

        card.save()
        return card
