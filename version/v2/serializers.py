from djoser.serializers import UserCreateSerializer
from rest_framework import  serializers


class CreateUserSerializer(UserCreateSerializer):
    '''Overriding Create user serializer
        this serializer does not return users id'''

    class Meta(UserCreateSerializer.Meta):
        fields = ["full_name", "email", "password"]
