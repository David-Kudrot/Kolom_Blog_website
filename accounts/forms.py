from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserAccountModel

# ekhane form tai user_category te fist tuple ('', 'Select User Category') use korsi tobe option a eta show korbe but kono value asbe na, niser gulo asbe and image a required=False use korsi upload korte pare abr nao pare but pore profile pic a click korle upload korte parbe
class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'id' : 'required'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'id' : 'required'}))
    user_category = forms.ChoiceField(choices=[('', 'Select User Category'), ('admin', 'Admin'), ('author', 'Author'), ('reader', 'Reader')],
                                      widget=forms.Select(attrs={'id': 'required'}))
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'user_category', 'profile_picture']
        
        
        

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = UserAccountModel
        fields = ['profile_picture']

        
            