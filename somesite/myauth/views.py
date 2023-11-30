from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView

from myauth.models import UserProfile


def log_out_user(request: HttpRequest):
    logout(request)
    return redirect(reverse('myauth:login'))


class MyLogoutView(LogoutView):
    """
    Класс реализует выход пользователя из учётной записи
    """
    # страница, куда будет перенаправлен пользователь после разлогирования
    next_page = reverse_lazy("myauth:login")


class AboutMeView(TemplateView):
    """
    Класс реализует страницу с данными пользователя
    """
    template_name = "myauth/about-me.html"


class UserRegisterView(CreateView):
    """
    Класс реализует регистрацию нового пользователя
    """
    template_name = "myauth/user-register.html"
    # получаем дефолтную форму для создания/регистрации нового пользователя
    form_class = UserCreationForm
    success_url = reverse_lazy("myauth:about-me")

    def form_valid(self, form):
        """
        Функция авторизует пользователя
        """
        # переопределяем родительский метод
        response = super().form_valid(form)
        UserProfile.objects.create(user=self.object)
        # получаем введённые пользователем пароль и логин
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")

        # функция authenticate() вернёт None, если данные не валидны для пароля
        # и вернёт пользователя, если данные валидны
        user = authenticate(
            self.request,
            password=password,
            username=username,
        )

        # авторизация пользователя
        login(self.request, user=user)
        return response
