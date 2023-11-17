import django.contrib.auth
import django.test
import django.urls

import users.models

__all__ = []


class MiddlewareTests(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = django.contrib.auth.get_user_model().objects.create_user(
            "tester",
            "tester@tst.ts",
            "jklhknkml!vc,;",
        )

    @django.test.override_settings(ALLOW_REVERSE=True)
    def test_coffee_endpoint_with_allowed_reverse(self):
        client = django.test.Client()
        contents = {client.get("/coffee/").content for _ in range(10)}
        self.assertIn("Я чайник".encode(), contents)
        self.assertIn("Я кинйач".encode(), contents)

    @django.test.override_settings(ALLOW_REVERSE=False)
    def test_coffee_endpoint_with_disabled_reverse(self):
        client = django.test.Client()
        contents = {client.get("/coffee/").content for _ in range(10)}
        self.assertIn("Я чайник".encode(), contents)
        self.assertNotIn("Я кинйач".encode(), contents)

    def test_instatnce_of_request_user(self):
        client = django.test.Client()
        client.login(username="tester", password="jklhknkml!vc,;")

        user_context = client.get(
            django.urls.reverse("homepage:home"),
        ).context["user"]
        self.assertIsInstance(user_context, users.models.ProxyUser)
