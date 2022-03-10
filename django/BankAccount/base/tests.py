from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model

from base.models import Address



TEST_ADMIN = {
    'username': 'admin',
    'first_name': 'Admin',
    'last_name': 'Admin',
    'password': 'admin',
    'email': 'admin@example.com',
    'identity_number': '123456789',
    'date_of_birth': '1980-01-01'
}



TEST_USER = {
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



class Base(TestCase):

    @classmethod
    def setUpClass(cls) -> None:

        super().setUpClass()

        user_model = get_user_model()

        cls.admin = user_model.objects.create_superuser(**TEST_ADMIN)

        with patch('base.models.get_current_user', return_value=cls.admin):

            address = Address.objects.create(**TEST_USER['address'])
            cls.user = user_model.objects.create(
                **{key: val for key, val in TEST_USER.items() if key != 'address'}, 
                address=address
            )


    def test_1_base_fields_after_create(self) -> None:
        """
        Check if create/write dates and uid are filled after creating a record
        """
       
        for field in ['create_date', 'write_date', 'create_uid', 'write_uid']:

            self.assertIsNotNone(
                getattr(self.user, field)
            )

        self.assertEquals(self.user.create_uid, self.admin)
        self.assertEquals(self.user.write_uid, self.admin)


    def test_2_base_fields_after_modify(self) -> None:
        """
        Check if modify date is changing after record modification and 
        create date is the same
        """

        write_uid = self.user.write_uid
        create_uid = self.user.create_uid
        write_date = self.user.write_date
        create_date = self.user.create_date

        self.user.first_name = 'John'
        self.user.save()

        self.assertNotEquals(write_date, self.user.write_date)
        self.assertEquals(create_date, self.user.create_date)
        self.assertNotEquals(write_uid, self.user.write_uid)
        self.assertEquals(create_uid, self.user.create_uid)


    def test_3_address_delete(self):
        """
        Check if address object will be delete on user deletion
        """

        self.user.delete()

        self.assertEquals(Address.objects.count(), 0)