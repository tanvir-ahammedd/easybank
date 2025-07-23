from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount',]
       
    # if we dont mention transaction_type in fields we dont need this  
    # def __init__(self, args, **kwargs):
    #     self.account = kwargs.pop('account')
    #     super().__init__(self, args, **kwargs)
    #     self.fields['transaction_type'].disabled = True
    #     self.fields['transaction_type'].widget = forms.HiddenInput
        
    def save(self, commit=True):
        self.instance.account = self.account
        self.instance.balance_after_transaction = self.account.balance
        return super().save()
    
class DepositForm(TransactionForm):
    
    def clean_amount(self):
        min_deposit_amount = 100
        amount = self.cleaned_data.get('amount')
        
        if amount < min_deposit_amount:
            raise forms.ValidationError(
                f'You need to deposit atleast {min_deposit_amount}$'
            )
        return amount

class WithdraForm(TransactionForm):
    def clean_amount(self):
        account = self.account
        min_withdraw_amount = 150
        max_withdraw_amount = (
            account.account_type.maximum_withdrawl_amount
        )
        balance = account.balance
        amount = self.cleaned_data.get('amount')
        if amount < min_withdraw_amount:
            raise forms.ValidationError(
                f'You can withdraw at least {min_withdraw_amount}'
            )
        if amount > max_withdraw_amount:
            raise forms.ValidationError(
                f'You can withdraw at max {max_withdraw_amount}'
            )
        if amount > balance:
            raise forms.ValidationError(
                f'You have {balance} in your account. '
                'You cant withdraw more than you account balance'
            )
            
class LoanRequestForm(TransactionForm):
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        
        return amount