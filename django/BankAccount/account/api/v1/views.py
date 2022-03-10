from django.db.models import Q
from django.core import exceptions
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from account.models import Account, Transaction
from base.api.v1.permissions import IsSuperUser
from .serializers import (
    AccountSerializer, 
    TransactionSerializer, 
    TransferSerializer
)
from .permissions import IsSelf



class AccountViewSet(viewsets.ModelViewSet):

    queryset = Account.objects.all().order_by('-create_date')

    serializer_class = AccountSerializer

    action_permissions = {
        'list': (IsAuthenticated, ), 
        'create': (IsAuthenticated, ), 
        'destroy': (IsSuperUser, ), 
        'update': (IsSuperUser, ),
        'retrieve': (IsSelf, ), 
        'partial_update': (IsSuperUser, ), 
        'transfer': (IsSelf, ),
        'history': (IsSelf, )
    }


    def get_permissions(self):

        return [
            permission() for permission \
                in self.action_permissions.get(self.action, [IsAuthenticated])
        ]


    def get_queryset(self):
        """
        Superusers retreive all accounts, the rest of user only accounts 
        assigned to them
        """

        if self.request.user.is_superuser:

            return super().get_queryset()

        return Account.objects.filter(
            user=self.request.user
        ).order_by('-create_date')


    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):

        account = self.get_object()

        transactions = Transaction.objects \
            .select_related('from_account') \
            .select_related('to_account') \
            .filter(
                Q(from_account=account) | Q(to_account=account)
            ).order_by('-create_date')

        page = self.paginate_queryset(transactions)

        if page is not None:
            serializer = TransactionSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = TransactionSerializer(transactions, many=True)
        result = [x.values()[0] for x in serializer.data]
        
        return Response(result)

    
    @action(detail=True, methods=['post'])
    def transfer(self, request, pk=None):

        account = self.get_object()

        serializer = TransferSerializer(data=request.data)

        if serializer.is_valid():

            try:
                account.transfer(
                    to_ban=serializer.validated_data['to_ban'],
                    amount=serializer.validated_data['amount'],
                    name=serializer.validated_data['name'],
                    title=serializer.validated_data['title']
                )
                return Response(status=status.HTTP_200_OK)

            except exceptions.ValidationError as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )

        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )