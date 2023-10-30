import django.test

__all__ = []


class MiddlewareTests(django.test.TestCase):
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
