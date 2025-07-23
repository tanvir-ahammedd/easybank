from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, RedirectView
from .forms import UserRegistrationForm, UserAddressForm

User = get_user_model()

class UserRegistrationView(TemplateView):
    model = User
    form_class = UserRegistrationForm
    template_name = ""
    # dispatch will preprocess data
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy(""))
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        registrationform = UserRegistrationForm(self.request.POST)
        addressform = UserAddressForm(self.request.POST)
        if registrationform.is_valid() and addressform.is_valid():
            user = registrationform.save()
            address = addressform.save()
            
            login(self.request.user)
            messages.success(self.request, (f"Thanks for creating account in our bank.. Your Account No is {user.account.account_no}"))
            return HttpResponseRedirect(reverse_lazy(""))
        
        # show form to the user 
        return self.render_to_response(
            self.get_context_data(
                registrationform = registrationform,
                addressform = addressform
            )
        )
    
    # initially kwargs is empty
    def get_context_data(self, **kwargs):
        if 'registration_form' not in kwargs:
            kwargs['registration_form'] = UserRegistrationForm
        if 'address_form' not in kwargs:
            kwargs['address_form'] = UserAddressForm
            
        return super().get_context_data(**kwargs)
    
class UserLoginView(LoginView):
    template_name = ""
    redirect_authenticated_user = False

class LogOutView(RedirectView):
    pattern_name = "" # after logout which page the user will go
    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
        return super().get_redirect_url(*args, **kwargs)