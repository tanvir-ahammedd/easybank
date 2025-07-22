from django.urls import path

from .views import UserRegistrationView, UserLoginView, LogOutView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name="user-registration"),
    path('logout/', LogOutView.as_view(), name="user-logout"),
    path('login/', UserLoginView.as_view(), name="user-login"),
]
