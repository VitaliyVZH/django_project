from django.test import TestCase
from django.urls import reverse


class MyauthBaseTestCase(TestCase):
    """
    Класс тестирует базовый View приложения myauth
    """
    def test_myauth_base(self):
        # получение ответа страницы
        response = self.client.get(reverse("myauth:base"))
        # проверка ответа на содержание статуса кода 200
        self.assertEqual(response.status_code, 200)
