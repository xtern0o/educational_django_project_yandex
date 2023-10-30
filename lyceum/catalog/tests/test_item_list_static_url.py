from http import HTTPStatus

import django.urls


__all__ = []


class StaticItemListTest(django.test.TestCase):
    def test_catalog_endpoint(self):
        response = django.test.Client().get(
            django.urls.reverse("catalog:item_list"),
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
