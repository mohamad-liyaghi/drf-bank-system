from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from .models import Card
import json

from v1.models import User

class API_Test(APITestCase):

    def setUp(self):
        '''
            First we create a user in our test db
        '''
        # create a new user
        user = User.objects.create_user(
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
