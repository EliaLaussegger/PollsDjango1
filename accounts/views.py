from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.utils import timezone
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import EmailMessage
import random
from profiles.models import Profile
from django.utils.crypto import get_random_string
import uuid
from django.contrib import messages
import time
from django.core.validators import validate_email
from django.core.exceptions import ValidationError




def register(request):
 if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        
        if username and password:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Benutzername existiert bereits.")
                return render(request, "accounts/register.html")


            user = User.objects.create_user(username=username, password=password, email=email)
            Profile.objects.create(user=user)
            user.save()
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('accounts:verification')
        return render(request, 'accounts/register.html')

def verification(request):
    if request.method == 'POST':
        saved_code = request.session.get("verification_code")
        user = request.user  
        profile = user.profile  
        code = request.POST.get("code")
        if code == saved_code:
            profile.is_verified = True
            profile.save()
            return redirect('polls:index')
        else:
            return render(request, 'accounts/verification.html', {
                'error': 'Code ist ungültig.'
            })
    return render(request, 'accounts/verification.html')


class RegisterView(TemplateView):
    template_name = "accounts/register.html"

class LoginView(TemplateView):
    template_name = "accounts/login.html"


class IndexView(TemplateView):
    template_name = "accounts/index.html"


class VerificationView(TemplateView):
    template_name = "accounts/verification.html"

    def get(self, request, *args, **kwargs):
        last_sent = request.session.get("last_email_sent", 0)
        now = time.time()
    
        if now - last_sent > 60:  # z. B. 60 Sekunden Sperre
            self.sendEmail(request)
            request.session["last_email_sent"] = now
    
        return super().get(request, *args, **kwargs)
    def sendEmail(self, request):
        user = request.user
        try:
            validate_email(user.email)  
        except ValidationError:
            print("Ungültige E-Mail-Adresse:", user.email)
        return HttpResponse("Ungültige E-Mail-Adresse.")
        try:
            profile = user.profile
            token = uuid.uuid4()
            profile.login_token = token
            profile.save()

            link = request.build_absolute_uri(
                reverse("accounts:login_with_token", args=[token])
            )

            if user.is_authenticated:
                code = str(random.randint(100000, 999999))
                request.session['verification_code'] = code     
                email = EmailMessage(
                    subject='HTML Nachricht',
                    body=f'<h1>Verifizierung</h1><p>Dein Code lautet: <strong>{code}</strong></p><p>"Klicke hier zum Einloggen: {link}<p>',
                    from_email='elia.laussegger@gmail.com',
                    to=[user.email],
            )
            email.content_subtype = 'html'
            email.send()
        except Profile.DoesNotExist:
            return HttpResponse("Kein Benutzer mit dieser E-Mail gefunden.")
    # def sendEmail(self, request):
    #     user = request.user
        
    #     if user.is_authenticated:
    #         code = str(random.randint(100000, 999999))
    #         request.session['verification_code'] = code     
    #         email = EmailMessage(
    #             subject='HTML Nachricht',
    #             body=f'<h1>Verifizierung</h1><p>Dein Code lautet: <strong>{code}</strong></p>',
    #             from_email='elia.laussegger@gmail.com',
    #             to=[user.email],
    #         )
    #         email.content_subtype = 'html'
    #         email.send()



def login_with_token(request, token,  backend='django.contrib.auth.backends.ModelBackend'):
    try:
        profile = Profile.objects.get(login_token=token)
        user = profile.user
        profile.login_token = None
        profile.is_verified = True
        profile.save()
        auth_login(request, user, backend=backend)
        return redirect("polls:index")
    except Profile.DoesNotExist:
        return HttpResponse("Ungültiger oder abgelaufener Token.")
    

def login_view(request, backend='django.contrib.auth.backends.ModelBackend'):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user, backend=backend)
            return redirect("polls:index")
        else:
            
            return render(request, "accounts/login.html", {
                "error": "Ungültiger Benutzername oder Passwort"
            })
    else:
        return render(request, "accounts/login.html") 

# def login_with_token(request, token):
#     try:
#         profile = Profile.objects.get(login_token=token)
#         user = profile.user
#         auth_login(request, user)
#         return redirect('polls:index')
#     except Profile.DoesNotExist:
#         return HttpResponse("Ungültiger Token")