from django.contrib import admin
from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views

app_name = "account"
urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("", views.IndexView.as_view(), name="index"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("new_login/", views.login_view, name="new_login"),
    path("new_register/", views.register, name="new_register"),
    path("verification/",views.VerificationView.as_view() ,name="verification"),
    path("verification_action/",views.verification ,name="verification_action"),
    path("send_login_link/", views.VerificationView.sendEmail, name="send_login_link"),
    path("login_with_token/<uuid:token>/", views.login_with_token, name="login_with_token"),
    # path("/accounts/login_with_token/<token>/", views.login_with_token, name="login_with_token"),

]