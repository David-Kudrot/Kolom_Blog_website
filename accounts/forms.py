from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserAccountModel


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'id' : 'required'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'id' : 'required'}))
    user_category = forms.ChoiceField(choices=[('', 'Select User Category'), ('admin', 'Admin'), ('author', 'Author'), ('reader', 'Reader')],
                                      widget=forms.Select(attrs={'id': 'required'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'user_category']
        
            