from django.core import exceptions
from django.db.utils import IntegrityError
from django.contrib.auth import password_validation as validators
from rest_framework import serializers

from account.models import Account, Transaction
from base.models import User
from base.api.v1.serializers import AddressSerializer



class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = '__all__'

    

class UserSerializer(serializers.ModelSerializer):

    address = AddressSerializer()

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'address'
        ]



class TransactionSerializer(serializers.ModelSerializer):

    from_user = UserSerializer(source='from_account.user')
    to_user = UserSerializer(source='to_account.user')

    class Meta:
        model = Transaction
        fields = '__all__'



class TransferSerializer(serializers.ModelSerializer):

    to_ban = serializers.CharField(required=True)
    amount = serializers.FloatField(required=True)
    name = serializers.CharField(required=True)
    title = serializers.CharField(required=True)

    class Meta:
        model = Transaction
        fields = [
            'to_ban',
            'amount',
            'name',
            'title'
        ]