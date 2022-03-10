import re

from typing import Generator

from django.db import models, transaction, IntegrityError, InternalError
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from base.models import Base



class Account(Base):

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT
    )

    balance = models.FloatField(_('Balance'), default=0.0)

    currency = models.CharField(
        _('Currency'),
        choices=settings.CURRENCIES, 
        default='pln',
        max_length=3
    )

    max_debit = models.FloatField(_('Max debit'), default=100.0)

    ban = models.CharField(
        _('Bank account number'), 
        max_length=32, 
        unique=True
    )


    @property
    def iban(self) -> str:

        return f'{settings.COUNTRY_CODE}{self.ban}'

    
    def save(self, *args, **kwargs) -> None:

        if not self.pk:
            self.ban = self.generate_ban()

        super().save(*args, **kwargs)

        if not self.user:
            self.user = self.create_uid
            self.save()

    
    @transaction.atomic
    def transfer(self, to_ban: str, amount: float, name: str, 
                    title: str) -> None:
        """
        
        """

        if amount < 0:

            raise ValidationError(
                _('Amount must be greater than 0')
            )

        if amount > self.balance + self.max_debit:

            raise ValidationError(_('You have not enough funds'))

        if not self.valid_ban(to_ban):

            raise ValidationError(_(f'BAN {to_ban} is not correct'))

        Transaction.objects.create(
            from_account=self,
            from_ban=self.ban,
            to_ban=to_ban,
            amount=amount,
            title=title,
            name=name,
            currency=self.currency
        )


    @classmethod
    def generate_ban(cls) -> str:

        # Customer number is number of all accounts in the system with leading 
        # zeros, first account will have 0000 0000 0000 0000 as customer number
        # If number of accounts reaches the limit, then raise
        customer = str(cls.objects.count())
        if len(customer) > 16:
            raise InternalError('Max number of accounts reached')

        customer = str(cls.objects.count()).zfill(16)

        # Change letter in country to numbers: A - 10, B - 11, C - 12 ...
        country_code = ''.join([
            str(ord(char) - 55) for char in settings.COUNTRY_CODE.upper()
        ])

        # Compose temp BAN with country code and two zeros at the end
        ban = f'{settings.BANK_ID}{settings.BRANCH_ID}' \
                f'{customer}{country_code}00'

        # Compute checksum (98 - ban % 97)
        # First split into two equal parts to avoid computing on large numbers
        first, second = ban[:len(ban)//2], ban[len(ban)//2:]
        first = str(int(first) % 97)
        checksum = str(98 - (int(first + second) % 97)).zfill(2)
        
        return f'{checksum}{settings.BANK_ID}{settings.BRANCH_ID}{customer}'


    @classmethod
    def valid_ban(self, ban: str) -> bool:

        if ban[0].isnumeric():

            ban = f'{settings.COUNTRY_CODE}{ban}' 

        # Remove non alpha-numeric characers
        ban = re.sub(r'\W+', '', ban)

        # Change letter in country to numbers: A - 10, B - 11, C - 12 ...
        ban = ''.join([
            str(ord(char) - 55) for char in ban[:2].upper()
        ]) + ban[2:]

        # Move first 6 chars to the end of the number
        ban = ban[6:] + ban[:6]

        if int(ban) % 97 == 1:

            return True

        return False
        


class Transaction(Base):


    from_account = models.ForeignKey(
        Account, 
        models.PROTECT, 
        verbose_name=_('From account'),
        related_name='from_account'
    )

    to_account = models.ForeignKey(
        Account, 
        models.PROTECT, 
        verbose_name=_('To account'),
        related_name='to_account'
    )

    from_ban = models.CharField(_('From bank account number'), max_length=32)

    to_ban = models.CharField(_('To bank account number'), max_length=32)

    outer = models.BooleanField('Outer transfer')

    currency = models.CharField(
        _('Currency'),
        choices=settings.CURRENCIES, 
        default='pln',
        max_length=3
    )

    amount = models.FloatField(_('Amount'))

    title = models.CharField(_('Title'), max_length=255)

    name = models.CharField(_('Name and address'), max_length=255)


    def save(self, *args, **kwargs):
        """
        Prevent from modyfing records and validate fields
        """

        if self.pk:

            raise IntegrityError(
                _('You can only add new transactions or read them')
            )

        if not Account.valid_ban(self.from_ban):

            raise ValidationError(_(f'BAN {self.from_ban} is not correct'))
        
        if not Account.valid_ban(self.to_ban):

            raise ValidationError(_(f'BAN {self.to_ban} is not correct'))

        if self.from_ban == self.to_ban:

            raise ValidationError(
                _('You cannot make a transfer within same account')
            )

        if self.amount < 0:

            raise ValidationError(
                _('Amount must be greater than 0')
            )

        self.outer = self.check_outer()

        if not self.outer:

            self.to_account = Account.objects.get(ban=self.to_ban)

        super().save(*args, **kwargs)

        self.from_account.balance -= self.amount
        self.from_account.save()

        if self.to_account:
            self.to_account.balance += self.amount
            self.to_account.save()


    def check_outer(self) -> bool:
        """
        Check if transfer is to another bank
        """

        return self.to_ban[2:6] != settings.BANK_ID

    
    def delete(self):

        raise IntegrityError(
            _('You can only add new transactions or read them')
        )

