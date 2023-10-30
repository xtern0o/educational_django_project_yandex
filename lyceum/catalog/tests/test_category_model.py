import django.core.exceptions
import django.test
import parameterized

import catalog.models


__all__ = []


class CatalogCategoryModelTest(django.test.TestCase):
    @parameterized.parameterized.expand([("a" * 151,), ("b" * 160,), ("",)])
    def test_create_category_unable_name(self, name):
        category_count = catalog.models.Category.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.cat = catalog.models.Category(name=name, slug="some-slug")
            self.cat.full_clean()
            self.cat.save()

        self.assertEqual(
            category_count,
            catalog.models.Category.objects.count(),
        )

    @parameterized.parameterized.expand([("a" * 150,), ("b" * 58)])
    def test_create_category_correct_name(self, name):
        category_count = catalog.models.Category.objects.count()
        self.cat = catalog.models.Category(
            name=name,
            slug="some-slug",
        )
        self.cat.full_clean()
        self.cat.save()

        self.assertEqual(
            category_count + 1,
            catalog.models.Category.objects.count(),
        )

    @parameterized.parameterized.expand(
        [("s" * 201,), ("f" * 300,), ("s0me_b@d slug",), ("s%233 ",)],
    )
    def test_create_category_unable_slug(self, slug):
        category_count = catalog.models.Category.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.cat = catalog.models.Category(name="aaa", slug=slug)
            self.cat.full_clean()
            self.cat.save()

        self.assertEqual(
            category_count,
            catalog.models.Category.objects.count(),
        )

    def test_create_category_with_duplicated_slug(self):
        category_count = catalog.models.Category.objects.count()
        self.cat = catalog.models.Category(name="test", slug="good-slug")
        self.cat.full_clean()
        self.cat.save()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.cat1 = catalog.models.Category(
                name="test name",
                slug="good-slug",
            )
            self.cat1.full_clean()
            self.cat1.save()

        self.assertEqual(
            category_count + 1,
            catalog.models.Category.objects.count(),
        )

    @parameterized.parameterized.expand(
        [("good-slug",), ("good_slug-example")],
    )
    def test_create_category_correct_slug(self, slug):
        category_count = catalog.models.Category.objects.count()
        self.cat = catalog.models.Category(name="name", slug=slug)
        self.cat.full_clean()
        self.cat.save()

        self.assertEqual(
            category_count + 1,
            catalog.models.Category.objects.count(),
        )

    @parameterized.parameterized.expand([(-1,), (-324,), (32768,), (35000,)])
    def test_create_category_unable_weight(self, weight):
        category_count = catalog.models.Category.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.cat = catalog.models.Category(
                name="test_name",
                slug="some-slug",
                weight=weight,
            )
            self.cat.full_clean()
            self.cat.save()

        self.assertEqual(
            category_count,
            catalog.models.Category.objects.count(),
        )

    @parameterized.parameterized.expand([(200,), (32767,)])
    def test_create_category_correct_weight(self, weight):
        category_count = catalog.models.Category.objects.count()
        self.cat = catalog.models.Category(
            name="test_name",
            slug="some-slug",
            weight=weight,
        )
        self.cat.full_clean()
        self.cat.save()

        self.assertEqual(
            category_count + 1,
            catalog.models.Category.objects.count(),
        )

    @parameterized.parameterized.expand(
        [
            ("новая кaтегор", "новая категор"),
            ("новая category", "новая саtegory"),
        ],
    )
    def test_create_cats_with_similar_normalized_names(self, name1, name2):
        self.cat = catalog.models.Category(name=name1, slug="slug1")
        self.cat.full_clean()
        self.cat.save()

        cat_count = catalog.models.Category.objects.count()

        with self.assertRaises(django.core.exceptions.ValidationError):
            self.cat1 = catalog.models.Category(name=name2, slug="slug2")
            self.cat1.full_clean()
            self.cat1.save()

        self.assertEqual(cat_count, catalog.models.Category.objects.count())
