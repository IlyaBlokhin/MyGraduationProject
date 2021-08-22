from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('first_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'type': "text", 'class': "form-control", 'id': "firstName", 'name': ''}),
            'email': forms.TextInput(attrs={'type': "email", 'class': "form-control", 'id': "email", 'placeholder': "you@example.com"})
        }


class PayOrder(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('paid',)


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

