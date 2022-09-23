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


class TransactionManager(models.Manager):
    '''
        Override create function
    '''

    def create(self, card_model, user, from_card, cvv, password, to_card, amount):
        # the card_model is not a good idea, this might be a bug, i have to fix it.

        if not card_model:
            raise ValueError("Model is required")

        if not user:
            raise ValueError('Transaction must have a user')

        if not from_card:
            raise ValueError("Transaction must have an origin ")

        if not cvv:
            raise ValueError("You must enter your cvv")

        if not password:
            raise ValueError("Password field is required")

        if not to_card:
            raise ValueError("Transaction must have a destination")

        if not amount:
            raise ValueError("You have to select amount of money to pay")

        origin = get_object_or_404(card_model, owner=user, number=from_card ,cvv= cvv, password= password )
        destination = get_object_or_404(card_model, number=to_card)

        if origin.balance < int(amount):
            raise ValueError("origin source doesnt have enough money")

        origin.balance -= int(amount)
        destination.balance += int(amount)
        origin.save()
        destination.save()

        transaction = self.model(
            code= random.randint(1, 9999999999999),
            from_card= origin,
            to_card= destination,
            amount= amount
        )

        transaction.save()
        return transaction