from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse


__all__ = ["StaticURLTests"]


class StaticURLTests(TestCase):
    def test_about_endpoint(self):
        response = Client().get(reverse("about:description"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
