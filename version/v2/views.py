from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from core.models import Card, Transaction
from v2.serializers import CardListSerializer, CreateCardSerializer, CardDetailSerializer, TransactionListSerializer


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

    def get_serializer_context(self):
        return {"user" : self.request.user}


    @action(detail=True, methods=["GET"], url_path="transactions")
    def get_card_transaction(self, request, token):
        """Return transactions related to a card"""

        card = get_object_or_404(Card, owner=self.request.user, token=token)
        transactions = card.transactions.all()

        serializer = TransactionListSerializer(transactions, many=True)

        return Response(serializer.data)

