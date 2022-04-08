from algosdk.constants import address_len, hash_len
from django.db import models
from django.http import Http404

from app.models import User
from contracts.helpers import account_balance, account_transactions, passphrase_from_private_key

# Create your models here.
class Account(models.Model):
    """Base model class for standalone and wallet Algorand accounts."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=address_len)
    private_key = models.CharField(max_length=address_len + hash_len)
    created = models.DateTimeField(auto_now_add=True)

    @classmethod
    def instance_from_address(cls, address):
        """Return model instance from provided account address."""
        try:
            return cls.objects.get(address=address)
        except ObjectDoesNotExist:
            raise Http404

    @classmethod
    def accounts_from_user(cls, user):
        """Return model instances belonging to the given user."""
        return cls.objects.filter(user=user)

    def balance(self):
        """Return this instance's balance in microAlgos."""
        return account_balance(self.address)

    @property
    def passphrase(self):
        """Return account's mnemonic."""
        return passphrase_from_private_key(self.private_key)

    def transactions(self):
        """Return all the transactions involving this account."""
        return account_transactions(self.address)

    def __str__(self):
        """Account's human-readable string representation."""
        return self.address