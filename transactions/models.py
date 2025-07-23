from django.db import models

# Create your models here.

from accounts.models import UserBankAccount
from .constants import TRANSACTION_TYPE

class TransactionForm(models.Model):
    account = models.ForeignKey(UserBankAccount, on_delete=models.CASCADE, related_name='transaction', null=True, blank=True)
    amount = models.DecimalField(decimal_places=2, max_digits=10, null=False)
    balance_after_transaction = models.DecimalField(decimal_places=2, max_digits=10, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    loan_approaved = models.BooleanField(default=False)
    transaction_type = models.PositiveIntegerField(choices=TRANSACTION_TYPE, null=True)
    
    class Meta:
        ordering = ['timestamp']