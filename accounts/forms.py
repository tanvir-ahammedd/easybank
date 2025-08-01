from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import User, BankAccountType, UserBankAccount, UserAddress
from .constants import GENDER_CHOICE

class UserAddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        exclude = ['user']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class':(
                    'appearance-none block w-full bg-gray-200'
                    'text-gray-700 border border-gray-200 rounded'
                    'py-3 px-4 leadin-tight focus:outline-none'
                    'focus:bg-white focus:border-gray-500'
                )
            })

class UserRegistrationForm(UserCreationForm):
    account_type = forms.ModelChoiceField(
        queryset=BankAccountType.objects.all())
    gender = forms.ChoiceField(choices=GENDER_CHOICE)
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'on'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'autofocus': 'off'}))
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class':(
                    'appearance-none block w-full bg-gray-200'
                    'text-gray-700 border border-gray-200'
                    'rounded py-3 px-4 leadin-tight'
                    'focus:outline-none focus:bg-white'
                    'focus:border-gray-500'
                )
            })
    @transaction.atomic
    def save(self, commit = True):
        user = super().save(commit = False) 
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            account_type = self.cleaned_data.get('account_type')
            gender = self.cleaned_data.get('gender')
            birth_date =self.cleaned_data.get('birth_date')
            UserBankAccount.objects.create(
                user = user,
                gender = gender,
                birth_date = birth_date,
                account_type = account_type,
                account_no = (
                    user.id +
                    1000000
                )
            )
        return user
        
    