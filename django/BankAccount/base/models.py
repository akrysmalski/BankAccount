from django.apps import apps
from django.db import models, transaction
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from crum import get_current_user



class Base(models.Model):
    """
    Base abstract model containing fields to log who and when create/modify
    a record and if a record is active
    """

    active = models.BooleanField(default=True)

    create_uid = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='%(class)s_create_uid',
        on_delete=models.PROTECT,
        null=True
    )

    write_uid = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='%(class)s_write_uid',
        on_delete=models.PROTECT,
        null=True
    )
    
    create_date = models.DateTimeField(auto_now_add=True)

    write_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


    def save(self, *args, **kwargs):
        """
        Update modify/create dates and create/write uid on save
        """

        user = get_current_user()

        if not self.pk:
            self.create_uid = user

        self.write_date = timezone.now()
        self.write_uid = user

        return super().save(*args, **kwargs)



class Address(models.Model):

    street = models.CharField(_('Street'), max_length=256)

    number = models.CharField(_('Number'), max_length=32)

    postal_code = models.CharField(_('Postal code'), max_length=32)

    city = models.CharField(_('City'), max_length=128)

    country = models.CharField(_('Country'), max_length=64)

    class Meta:
        verbose_name = _('Address')



class User(AbstractUser, Base):
    """
    A simple bank user which owns one or more bank accounts, will be used
    also for authentication
    """

    identity_number = models.CharField(_('Identity number'), max_length=32, null=True)

    date_of_birth = models.DateField(_('Date of birth'), null=True)

    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = _('User')


    @property
    def accounts(self):

        model = apps.get_model('account.Account')

        return model.objects.filter(user=self).values_list('pk', flat=True)


    @transaction.atomic    
    def delete(self) -> None:

        if self.address:
            self.address.delete()

        return super().delete()

