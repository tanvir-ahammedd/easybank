from django.contrib import admin

# Register your models here.
from .models import BankAccountType, User, UserAddress, UserBankAccount

admin.site.register(BankAccountType)
admin.site.register(User)
admin.site.register(UserAddress)
admin.site.register(UserBankAccount)