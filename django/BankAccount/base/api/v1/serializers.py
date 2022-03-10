from django.core import exceptions
from django.db.utils import IntegrityError
from django.contrib.auth import password_validation as validators
from rest_framework import serializers

from base.models import User, Address
from account.models import Account



class ChangePasswordSerializer(serializers.Serializer):
    
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):

        user = self.context['request'].user

        try:
            validators.validate_password(password=value, user=user)

        except exceptions.ValidationError as e:
            raise serializers.ValidationError(
                {'password': list(e.messages)}
            )

        return value



class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = '__all__'



class UserSerializer(serializers.ModelSerializer):

    username = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    address = AddressSerializer(required=True)
    date_of_birth = serializers.DateField(required=True)
    identity_number = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = [
            'pk',
            'username', 
            'first_name', 
            'last_name', 
            'date_of_birth',
            'identity_number',
            'address',
            'password'
        ]
        read_only_fields = [
            'pk',
            'username', 
            'first_name', 
            'last_name', 
            'date_of_birth',
            'identity_number',
            'password'
        ]


    def to_representation(self, instance) -> dict:
        """
        Add ids of accounts assigned to this user
        """

        data = super().to_representation(instance)

        data['accounts'] = instance.accounts

        return data


    def create(self, data):

        address = data.pop('address')

        address = Address.objects.create(**address)

        user = User(**data, address=address)

        password = data.get('password')

        try:
            validators.validate_password(password=password, user=user)

        except exceptions.ValidationError as e:
            raise serializers.ValidationError(
                {'password': list(e.messages)}
            )

        user.set_password(data['password'])

        try:
            user.save()

        except IntegrityError as e:
            raise serializers.ValidationError(
                {'username': 'Username already exists'}
            )

        Account.objects.create(user=user)

        return user