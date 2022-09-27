from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from core.models import Card, Transaction
from v2.serializers import (CardListSerializer, CreateCardSerializer, CardDetailSerializer,
                            TransactionListSerializer, AddTransactionSerializer)


class CardViewSet(ModelViewSet):
    '''A viewset for add/update/delete a card'''

    permission_classes = [IsAuthenticated,]
    lookup_field = 'token'

    def get_queryset(self):
        # return all cards of a user.
        return Card.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        # serialize data with appropriate serializers
        if self.action == "list":
            return CardListSerializer

        elif self.action == "create":
            return CreateCardSerializer

        elif self.action in ["update", "partial_update", "delete", "retrieve", "metadata"]:
            return CardDetailSerializer

        elif self.action == "get_card_transaction":
            return TransactionListSerializer

        elif self.action == "add_transaction":
            return AddTransactionSerializer

    def get_serializer_context(self):
        return {"user" : self.request.user}


    @action(detail=True, methods=["GET"], url_path="transactions")
    def get_card_transaction(self, request, token):
        """Return transactions related to a card"""

        card = get_object_or_404(Card, owner=self.request.user, token=token)
        transactions = card.transactions.all()

        serializer = TransactionListSerializer(transactions, many=True)

        return Response(serializer.data)

    @action(detail=False, methods=['post', 'get'], url_path="add-transaction")
    def add_transaction(self, request):
        '''Add a new transaction in order to pay money'''

        if request.method == "POST":
            serializer = AddTransactionSerializer(data=request.data)

            if serializer.is_valid():
                vd = serializer.validated_data

            try:
                transaction = Transaction.objects.create(Card, user=self.request.user,
                                           from_card=vd["origin"], cvv=vd["cvv"],
                                           password=vd["password"], to_card=vd["destination"],
                                           amount=vd["amount"])

                serializer = TransactionListSerializer(transaction)
                return Response(serializer.data)

            except ValueError:
                return Response("Sth went wrong, please try again later. you may not have enough money in your card.")

            else:
                return Response(serializer.error)

        elif request.method == "GET":
            return Response("Create a Transaction here")



