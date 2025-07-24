from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.utils import timezone
from django.views.generic import ListView, CreateView
from datetime import datetime
from django.db.models import Sum
from django.urls import reverse_lazy
from transactions.constants import DEPOSIT, WITHDRAWL, LOAN, LOAN_PAID
from transactions.forms import (
    DepositForm,
    WithdraForm, 
    LoanRequestForm,
)

from .models import Transaction


class TransactionReportView(LoginRequiredMixin, ListView):
    template_name = 'transactions/transaction_report.html'
    model = Transaction
    form_data = {}
    balance = 0

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            account=self.request.user.account
        )

        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')

        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() 
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

            queryset = queryset.filter(
                timestamp_date__gte=start_date,     
                timestamp_date__lte=end_date          
            )

            self.balance = queryset.aggregate(Sum('amount'))['amount__sum'] or 0
        else:
            self.balance = self.request.user.account.balance

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'account': self.request.user.account
        })
        return context

class TransactionCreateMixin(LoginRequiredMixin, CreateView):
    template_name = 'transactions/transaction_form.html'
    model = Transaction
    title = ''
    success_url = reverse_lazy('transaction_report')
    
    # To send extra data to your form that Django wouldn't automatically send
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user.account
        })
        return kwargs
    
    # To pass extra variables to the HTML template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title
        })
        return context
    
class DepositMoneyView(TransactionCreateMixin):
    form_class = DepositForm
    title = 'Deposit'
    
    def get_initial(self):
        initial = {'transaction_type': DEPOSIT}
        return initial
    
    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        
        if not account.initial_deposit_date:
            now = timezone.now()
            account.initial_deposit_date = now
        account.balance += amount
        account.save(
            update_fields=[
                'inittial_deposit_date',
                'balance'
            ]
        )
        formatted_amount = f"{float(amount):,.2f}"
        messages.success(
            self.request,
            f'{formatted_amount}$ was deposited to your account successfully'
        )
        return super().form_valid(form)
 
class WithdrawMoneyView(TransactionCreateMixin):
    form_class = WithdraForm
    title = 'Withdraw Money'
    
    def get_initial(self):
        initial = {'transaction_type': WITHDRAWL}
        return initial
    
    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        self.request.user.account.balance -= amount
        self.request.user.save(update_fields=['balance'])
        
        formatted_amount = f"{float(amount):,.2f}"
        messages.success(
            self.request,
            f'{formatted_amount}$ was deposited to your account successfully'
        )
        return super().form_valid(form)

class LoanRequestView(TransactionCreateMixin):
    form_class = LoanRequestForm
    title = 'Request For Loan'
    
    def get_initial(self):
        initial = {'transaction_type': LOAN}
        return initial
    
    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        current_loan_count = Transaction.objects.filter(
            account = self.request.user.account, transaction_type=3, loan_approve=True).count()
        
        if current_loan_count >= 3:
            return HttpResponse("you have cross the limit")
        
        formatted_amount = f"{float(amount):,.2f}"
        messages.success(
            self.request,
            f'{formatted_amount}$ was deposited to your account successfully'
        )
        return super().form_valid(form)
    
class PayLoanView(LoginRequiredMixin, View):
    def get(self, request, loan_id):
        loan = get_object_or_404(Transaction, id=loan_id)
        print(loan)
        if loan.loan_approaved:
            user_account = loan.account
            
            if loan.amount < user_account.balance:
                user_account.balance -= loan.amount
                loan.balance_after_transaction 
                loan.balance_after_transaction = user_account.balance
                user_account.save()
                loan.loan_approaved = True
                loan.transaction_type = LOAN_PAID
                loan.save()
                return redirect('transaction: loan_list')
            else:
                messages.error(
                    self.request,
                    f'Loan amount is greater than available balanace'   
                )
        return redirect('loan_list')
    
class LoanListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'tansactions/loan_request.html'
    context_object_name = 'loans'
    
    def get_queryset(self):
        user_account = self.request.user.account
        queryset = Transaction.objects.filter(account=user_account, transaction_type=3)
        print(queryset)
        return queryset

