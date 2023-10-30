import django.core.exceptions
import django.test
import parameterized

import catalog.models


__all__ = []


class CatalogItemModelTest(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category = catalog.models.Category.objects.create(
            name="Test cat",
            slug="test-cat",
        )
        cls.tag1 = catalog.models.Tag.objects.create(
            name="Test tag 1",
            slug="test-tag-1",
        )

    @parameterized.parameterized.expand(
        [("хороший текст",), ("роскошный не считается",), ("",), ("f" * 201,)],
    )
    def test_item_unable_text(self, text):
        item_count = catalog.models.Item.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.item = catalog.models.Item(
                name="name",
                text=text,
                category=CatalogItemModelTest.category,
            )
            self.item.full_clean()
            self.item.save()
            self.item.tags.add(CatalogItemModelTest.tag1)

        self.assertEqual(item_count, catalog.models.Item.objects.count())

    @parameterized.parameterized.expand(
        [
            ("хороший текст превосходно",),
            ("роскошно считается",),
            ("Роскошно",),
            ("роскошно!"),
        ],
    )
    def test_item_correct_text(self, text):
        item_count = catalog.models.Item.objects.count()
        self.item = catalog.models.Item(
            name="name",
            text=text,
            category=CatalogItemModelTest.category,
        )
        self.item.full_clean()
        self.item.save()
        self.item.tags.add(CatalogItemModelTest.tag1)

        self.assertEqual(item_count + 1, catalog.models.Item.objects.count())

    def test_item_empty_category(self):
        item_count = catalog.models.Item.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.item = catalog.models.Item(
                name="name",
                text="some превосходно роскошно text",
            )
            self.item.full_clean()
            self.item.save()
            self.item.tags.add(CatalogItemModelTest.tag1)

        self.assertEqual(item_count, catalog.models.Item.objects.count())
