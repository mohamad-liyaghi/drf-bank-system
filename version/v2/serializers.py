from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from core.models import Card


class CreateUserSerializer(UserCreateSerializer):
    '''Overriding Create user serializer
        this serializer does not return users id'''

    class Meta(UserCreateSerializer.Meta):
        fields = ["full_name", "email", "password"]


class CardListSerializer(serializers.ModelSerializer):
    '''List of users cards'''

    class Meta:
        model = Card
        fields = ["number", "cvv", "token"]


class CreateCardSerializer(serializers.ModelSerializer):
    '''create a card for a user'''
    token = serializers.CharField(read_only=True)

    class Meta:
        model = Card
        fields = ["password", "token"]

    def create(self, validated_data):
        # get user from the context
        user = self.context["user"]

        return Card.objects.create(owner=user, **validated_data)