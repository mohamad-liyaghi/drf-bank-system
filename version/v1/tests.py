from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from .models import Card, Transaction
import json

from v1.models import User

class API_Test(APITestCase):

    def setUp(self):
        '''
            First we create a user in our test db
        '''
        # create a new user
        self.user = User.objects.create_user(
            email= "test@test.com",
            full_name= "user fullname",
            password= "TestPass1234"
        )

        # request for new api token
        request = self.client.post(
            reverse("token_obtain_pair"),
            data={"email": "test@test.com", "password": "TestPass1234"},
            format="json"
        )

        data = json.dumps(request.data)
        dumped_data = json.loads(data)

        access_key = dumped_data["access"]
        # authenticate via token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_key}')


    def test_create_card(self):
        '''
            Create a new card for user.
        '''

        request = self.client.post(
            reverse("v1:create-card"),
            data={"password": "1234"},
            format="json"
        )

        card = Card.objects.filter(owner= self.user).first()

        # check if user have just one card
        self.assertEqual(self.user.cards.count(), 1)
        self.assertNotEqual(self.user.cards.count(), 2)

        # check the balance of a card
        self.assertEqual(card.balance, 0)
        self.assertNotEqual(card.balance, 100)


    def test_transaction(self):
        '''
            Transfer amount of money from old card to new card
        '''

        # Create a new card
        request_for_first_card = self.client.post(
            reverse("v1:create-card"),
            data={"password": "4321"},
            format="json"
        )

        second_card = Card.objects.create(self.user, "1234")
        # Change Second card number in order to fix a conflict
        second_card.number = "123456789"
        second_card.save()
        second_card.refresh_from_db()

        # get first card
        first_card = Card.objects.filter(owner=self.user, password= 4321).first()

        # Add 100$ to first card in order to transfer 50$ of that
        first_card.balance = 100
        first_card.save()

        self.assertEqual(first_card.balance, 100)
        self.assertEqual(second_card.balance, 0)

        # transfer money
        transaction = self.client.post(
            reverse("v1:create-transaction"),

            data= {
                "from_card" : first_card,
                "cvv" : first_card.cvv,
                "password" : first_card.password,
                "to_card" : second_card,
                "amount" : "50"
            },
            foramt= "json"
        )
        # refresh database
        first_card.refresh_from_db()
        second_card.refresh_from_db()

        self.assertEqual(transaction.status_code, 201)
        self.assertEqual(first_card.balance, 50)
        self.assertEqual(second_card.balance, 50)
