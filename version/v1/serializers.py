from  rest_framework import  serializers
from core.models import Card, User, Transaction

class RegisterUserSerializer(serializers.ModelSerializer):
    '''
        Create User serializer
    '''
    class Meta:
        model = User
        fields = ('id', "full_name", 'email', 'password')

        extra_kwargs = {'password': {'write_only': True},}

        def create(self, validated_data):
            '''
                Create user with serializer data
            '''
            user = User.objects.create_user(**validated_data)
            return user

class CreateCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ("password",)
        extra_kwargs = {'password': {'write_only': True},}

class ListCardSerializer(serializers.ModelSerializer):
    '''List of users cards.'''
    class Meta:
        model = Card
        fields = ("number", "token")

class DetailCardSerializer(serializers.ModelSerializer):
    '''
        Return extra detail about a card
    '''
    owner = serializers.CharField(source="owner.email")
    class Meta:
        model = Card
        fields = ("owner", "number", "cvv", "balance", "date_created", "token")


class ChangePasswordCardSerializer(serializers.ModelSerializer):
    '''
        Change password of a card
    '''
    old_password = serializers.CharField(required=True, max_length=8)
    new_password = serializers.CharField(required=True, max_length=8)
    class Meta:
        model = Card
        fields = ("old_password", "new_password")


class TransactionSerializer(serializers.ModelSerializer):

    cvv = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    from_card = serializers.CharField(required=True)
    to_card = serializers.CharField(required=True)

    class Meta:
        model = Transaction
        fields = ('from_card', 'to_card', 'amount','cvv', 'password',)


class TransactionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ("code", "amount", "date")


class TransactionDetailSerializer(serializers.ModelSerializer):
    from_card = serializers.CharField(source="from_card.number")
    to_card = serializers.CharField(source="from_card.number")

    class Meta:
        model = Transaction
        fields = ("code","from_card", "to_card" , "amount", "date")
