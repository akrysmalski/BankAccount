from unittest.mock import patch

from django.test import TestCase
from django.db import IntegrityError, InternalError
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth import get_user_model

from base.tests import TEST_ADMIN
from base.models import Address
from account.models import Account, Transaction



TEST_USER_1 = {
    'username': 'asmith123',
    'first_name': 'Alex',
    'last_name': 'Smith',
    'password': 'password',
    'email': 'alex.smith@example.com',
    'identity_number': 'CE1234567',
    'date_of_birth': '1980-01-01',
    'address': {
        'street': 'Street',
        'number': '12',
        'city': 'City',
        'postal_code': '12345-12',
        'country': 'Country'
    }
}

TEST_USER_2 = {
    'username': 'jwatson123',
    'first_name': 'John',
    'last_name': 'Watson',
    'password': 'password',
    'email': 'john.watson@example.com',
    'identity_number': 'CE1234567',
    'date_of_birth': '1980-01-01',
    'address': {
        'street': 'Street',
        'number': '12',
        'city': 'City',
        'postal_code': '12345-12',
        'country': 'Country'
    }
}

# This bank account number is correct
TEST_BAN = '49 1020 2892 2276 3005 0000 0000'



class TestAccount(TestCase):

    @classmethod
    def setUpClass(cls) -> None:

        super().setUpClass()

        user_model = get_user_model()

        cls.admin = user_model.objects.create_superuser(**TEST_ADMIN)

        with patch('base.models.get_current_user', return_value=cls.admin):

            address_1 = Address.objects.create(**TEST_USER_1['address'])
            cls.user_1 = user_model.objects.create(
                **{key: val for key, val in TEST_USER_1.items() if key != 'address'}, 
                address=address_1
            )

            address_2 = Address.objects.create(**TEST_USER_2['address'])
            cls.user_2 = user_model.objects.create(
                **{key: val for key, val in TEST_USER_2.items() if key != 'address'}, 
                address=address_2
            )

            cls.account_1 = Account.objects.create(user=cls.user_1)
            cls.account_2 = Account.objects.create(user=cls.user_2)


    def test_1_valid_ban(self) -> None:

        self.assertTrue(Account.valid_ban(TEST_BAN))


    def test_2_generate_ban(self) -> None:
       
        ban = Account.generate_ban()

        self.assertEquals(ban[-16:], '2'.zfill(16))
        self.assertEqual(ban[2:6], settings.BANK_ID)
        self.assertEqual(ban[6:10], settings.BRANCH_ID)

        self.assertTrue(Account.valid_ban(ban))

    
    def test_3_transfer_amount_less_than_zero(self) -> None:

        with self.assertRaises(ValidationError):

            self.account_1.transfer(
                to_ban=self.account_2.ban,
                amount=-50,
                name='Test',
                title='Test'
            )

    def test_4_transfer_not_enough_funds(self) -> None:

        with self.assertRaises(ValidationError):

            self.account_1.transfer(
                to_ban=self.account_1.ban,
                amount=150,
                name='Test',
                title='Test'
            )

    def test_5_transfer_ban_not_correct(self) -> None:

        with self.assertRaises(ValidationError):

            self.account_1.transfer(
                to_ban='0000000',
                amount=50,
                name='Test',
                title='Test'
            )

    def test_5_transfer(self) -> None:


        self.account_1.transfer(
            to_ban=self.account_2.ban,
            amount=50,
            name='Test',
            title='Test'
        )

        self.account_2 = Account.objects.get(pk=self.account_2.pk)

        self.assertEquals(self.account_1.balance, -50)
        self.assertEquals(self.account_2.balance, 50)