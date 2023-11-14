import django.conf
import django.test
import django.urls

import users.models


__all__ = []


class UsersTests(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.signup_data = {
            "email": "test@mail.ru",
            "username": "test_username_lol",
            "password1": "asdkl;u@MKF4",
            "password2": "asdkl;u@MKF4",
        }

        cls.active_user = users.models.ProxyUser.objects.create_user(
            username="active_user",
            email="test2@mail.com",
            password="passwoo231231",
            is_active=True,
        )

        cls.nonactive_user = users.models.ProxyUser.objects.create_user(
            username="nonactive_user",
            email="test3@mail.com",
            password="passwoo23231231",
            is_active=False,
        )

    def test_signup_successful(self):
        count = users.models.ProxyUser.objects.count()
        django.test.Client().post(
            django.urls.reverse("users:signup"),
            data=self.signup_data,
            follow=True,
        )
        self.assertEqual(count + 1, users.models.ProxyUser.objects.count())
