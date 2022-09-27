from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from core.models import Card, Transaction


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
    password = serializers.CharField(write_only=True)


    class Meta:
        model = Card
        fields = ["password", "token"]

    def create(self, validated_data):
        # get user from the context
        user = self.context["user"]

        return Card.objects.create(owner=user, **validated_data)


class CardDetailSerializer(serializers.ModelSerializer):
    '''Card detail page'''

    lookup_field = 'token'

    extra_kwargs = {
        'url': {'lookup_field': 'token'}
    }

    token = serializers.CharField(read_only=True)
    number = serializers.CharField(read_only=True)
    cvv = serializers.CharField(read_only=True)
    date_created = serializers.CharField(read_only=True)
    balance = serializers.CharField(read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Card
        fields = ["number", "cvv", "balance", "date_created", "token", "password"]


class TransactionListSerializer(serializers.ModelSerializer):
    '''Return Transactions of a card'''

    from_card = serializers.StringRelatedField()
    to_card = serializers.StringRelatedField()

    class Meta:
        model = Transaction
        fields = ["code", "from_card", "to_card", "date", "amount"]