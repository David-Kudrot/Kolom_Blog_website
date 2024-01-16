from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
# for sending email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import redirect
from django.contrib import messages

from django.contrib.auth.forms import  AuthenticationForm
from .models import UserAccountModel
#for logged out by deleting auth token
from django.contrib.auth import get_user_model

# Create your views here.


def register(request):
    if request.method == 'POST':
        register_form = RegistrationForm(request.POST)
        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.is_active=False
            user.save()
            
            #saving user category
            user_category = register_form.cleaned_data['user_category']
            UserAccountModel.objects.create(user=user, user_category=user_category)
            
            
            token = default_token_generator.make_token(user)
            print("token ", token)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            print("uid ", uid)
            confirm_link = f"http://127.0.0.1:8000/accounts/active/{uid}/{token}"
            email_subject = "Confirm Your Email"
            email_body = render_to_string('confirm_email.html', {'confirm_link' : confirm_link})
            
            email = EmailMultiAlternatives(email_subject , '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            messages.success(request, "We have send you an confirmation email.")
            return redirect('login')
    
    else:
        register_form =RegistrationForm()
    return render(request, 'register.html', {'form' : register_form, 'type' : 'Register'})



def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user = None 
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return redirect('register')
    
    
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['username']
            user_pass = form.cleaned_data['password']
            user = authenticate(username=user_name, password=user_pass)
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                print(token)
                print(_)
                login(request, user)
                return redirect('home')
            else:
                messages.warning(request, 'Login information incorrect')
                return redirect('register')
        else:
            messages.warning(request, 'Login information incorrect')
            return redirect('register')
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form' : form, 'type' : 'Sign in'})
    
    
    


def user_logout(request):
    if request.user.is_authenticated:
        User = get_user_model()
        try:
            # Check if the user has an associated auth_token
            auth_token = request.user.auth_token
            auth_token.delete()
        except User.auth_token.RelatedObjectDoesNotExist:
            pass  # No auth_token associated with the user
        
        logout(request)
        return redirect('login')