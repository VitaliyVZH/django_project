from django.contrib.auth.views import LoginView
from django.urls import path

from myauth.views import myauth_base, MyLogoutView, AboutMeView, UserRegisterView

app_name = 'myauth'
urlpatterns = [
    path("", myauth_base, name="base"),
    path('login/', LoginView.as_view(
        template_name="myauth/login.html",
        redirect_authenticated_user=True,
    ), name="login"),

    path("logout/", MyLogoutView.as_view(), name="logout"),
    path("about-me/", AboutMeView.as_view(), name="about-me"),
    path("register/", UserRegisterView.as_view(), name="register"),

]
