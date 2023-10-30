from http import HTTPStatus

import django.test
import django.urls


__all__ = []


class StaticURLTests(django.test.TestCase):
    def test_homepage_endpoint(self):
        response = django.test.Client().get(
            django.urls.reverse("homepage:home"),
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_coffee_endpoint(self):
        response = django.test.Client().get(
            django.urls.reverse("homepage:coffee"),
        )
        self.assertIn("Я чайник", response.content.decode("utf-8"))
        self.assertEqual(response.status_code, HTTPStatus.IM_A_TEAPOT)
