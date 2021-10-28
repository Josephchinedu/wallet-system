from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from accounts.models import User

import uuid

class Wallet(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    balance = models.DecimalField(_("balance"), max_digits=100, decimal_places=2)
    account_name = models.CharField(_("account name"), max_length=250)
    account_number = models.CharField(_("account number"), max_length=100)
    bank = models.CharField(_("bank"), max_length=100)
    phone_number = models.CharField(_("phone number"), max_length=15)
    password = models.CharField(_("password"), max_length=200)
    created = models.DateTimeField(auto_now_add=True)






class WalletTransaction(models.Model):
    class STATUS(models.TextChoices):
        PENDING = 'pending', _('Pending')
        SUCCESS = 'success', _('Success')
        FAIL = 'fail', _('Fail')

    class TransactionType(models.TextChoices):
        BANK_TRANSFER_FUNDING = 'funding', _('Bank Transfer Funding')
        BANK_TRANSFER_PAYOUT = 'payout', _('Bank Transfer Payout')
        DEBIT_USER_WALLET = 'debit user wallet', _('Debit User Wallet')
        CREDIT_USER_WALLET = 'credit user wallet', _('Credit User Wallet')

    transaction_id = models.CharField(_("transaction id"), max_length=250)
    status = models.CharField(max_length=200, null=True, 
        choices=STATUS.choices, 
        default=STATUS.PENDING
    )
    transaction_type = models.CharField(max_length=200, null=True,
        choices=TransactionType.choices
        )
    wallet = models.ForeignKey(Wallet, on_delete=models.SET_NULL, 
        null=True
    )
    amount = models.DecimalField(_("amount"), max_digits=100, decimal_places=2)
    date = models.CharField(_("date"), max_length=200)