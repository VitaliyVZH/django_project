from random import choices
from string import ascii_letters

from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse

from shopapp.models import Product


class ProductCreateViewTestCase(TestCase):
    """
    Класс тестирует создание нового продукта
    """
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create(username="Super Test Bob", password="qwerty")
        cls.permission = Permission.objects.all()

    def setUp(self) -> None:
        """
        Функция активируется в момент обращения к классу.
        Функция создаёт объект класса (имя продукта) с рандомными символами.
        Происходит удаление продукта, если такой же есть в базе
        """
        self.product_name = "".join(choices(ascii_letters, k=10))
        Product.objects.filter(name=self.product_name).delete()
        self.client.force_login(self.user)
        for perm in self.permission:
            self.user.user_permissions.add(perm)


    @classmethod
    def tearDownClass(cls) -> None:
        cls.user.delete()

    def test_product_create(self):
        """
        В функции-тесте совершается post запрос с передачей данных
        результат сохраняется в переменную response
        """
        response = self.client.post(
            reverse("shopapp:product_create"),
            {
                'name': self.product_name,
                'price': "10.5",
                'description': "",
            }
        )

        # проверка ответа на редирект к указанной странице и соответствующий код ответа
        self.assertRedirects(response, reverse("shopapp:products"))
        # проверка создания объекта
        self.assertTrue(Product.objects.filter(name=self.product_name).exists())


class ProductDetailsViewTestCase(TestCase):
    """
    Класс тестирует страницу с деталями продукта
    """
    @classmethod
    def setUpClass(cls):
        """
        Функция активируется в момент обращения к классу.
        В функции происходит создание публичных атрибутов класса:
         - создание продукта с рандомным названием;
         - создание нового пользователя.
        """

        cls.product = Product.objects.create(name="".join(choices(ascii_letters, k=10)))
        cls.user = User.objects.create_user(username='Best user', password="qwerty")

    @classmethod
    def tearDownClass(cls):
        """
        Метод класса. Этот метод запускается в самом конце, когда все методы и тесты в классе отработают.
        В этом методе удаляется ранее созданный продукт и пользователь
        """
        cls.product.delete()
        cls.user.delete()

    def setUp(self) -> None:
        """
        Функция запускается в начале работы класса.
        Производится аутентификация пользователя
        """
        self.client.force_login(self.user)

    def test_product_detail(self):
        """
        В функции производится запрос к странице с деталями продукта и проверяется,
        содержит ли ответ название созданного продукта.
        """
        response = self.client.get(
            reverse("shopapp:product_details", kwargs={'pk': self.product.pk})
        )
        self.assertContains(response, self.product.name)


class ProductListViewTestCase(TestCase):
    fixtures = [
        'shopapp_products-fixture.json',
    ]

    @classmethod
    def setUpClass(cls):
        """
        Функция активируется в момент обращения к классу.
        В функции происходит создание публичных атрибутов класса:
         - создание нового пользователя;
         - создание публичного атрибута класса ссылающегося на разрешение.
        """
        cls.user = User.objects.create_user(username='Best user', password="qwerty")
        cls.permission = Permission.objects.get(codename="view_product")

    @classmethod
    def tearDownClass(cls):
        """
        Этот метод запускается в самом конце, когда все методы и тесты в классе отработают.
        В этом методе удаляется ранее созданный пользователь.
        """
        cls.user.delete()

    def setUp(self) -> None:
        """
        Функция активируется в момент обращения к классу.
        Происходит аутентификация пользователя.
        Пользователю добавляется разрешение.
        """
        self.client.force_login(self.user)
        self.user.user_permissions.add(self.permission)

    def test_products_list(self):
        response = self.client.get(reverse("shopapp:products"))
        self.assertEqual(response.status_code, 200)
