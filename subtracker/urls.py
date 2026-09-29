from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from subscriptions.forms import LoginForm
from subscriptions.views import register, account_delete

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="registration/login.html", authentication_form=LoginForm),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", register, name="register"),
    path("account/delete/", account_delete, name="account_delete"),
    path("", include("subscriptions.urls")),
]
