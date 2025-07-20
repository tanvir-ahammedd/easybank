from django.db import models
from decimal import Decimal
from django.contrib.auth. models import AbstractBaseUser
from django.core.validators import (MinValueValidator, MaxLengthValidator)
from .managers import UserManager
from .constants import GENDER_CHOICE

class User(AbstractBaseUser):
    username = None
    email = models.EmailField(unique=True, null=False, blank=True)
    # all user objects will be handaled by the UserManager
    objects = UserManager
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email
    
    @property
    def balance(self):
        if hasattr(self, 'account'):
            return self.account.balance
        return 0
    
class BankAccountType(models.Model):
    name = models.CharField(max_length=30)
    maximum_withdrawl_amount = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return self.name
    
class UserBankAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    account_type = models.ForeignKey(BankAccountType, on_delete=models.CASCADE, related_name='accounts')
    account_no = models.PositiveIntegerField(unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE)
    birth_date = models.DateField(null=True, blank=True)
    initial_deposite_date = models.DateField(auto_now_add=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return self.account_no

class UserAddress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='address')
    street_address = models.CharField(max_length=100)
    city = models.CharField(50)
    postal_code = models.PositiveBigIntegerField()
    country = models.CharField(50)
    def __str__(self):
        return self.user.email