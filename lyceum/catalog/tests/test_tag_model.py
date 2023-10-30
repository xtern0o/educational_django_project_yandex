import django.core.exceptions
import django.test
import parameterized

import catalog.models


__all__ = []


class CatalogTagModelTest(django.test.TestCase):
    @parameterized.parameterized.expand([("t" * 151,), ("",), ("f" * 320,)])
    def test_create_tag_unable_name(self, name):
        tag_count = catalog.models.Tag.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.tag = catalog.models.Tag(name=name, slug="some-correct-slug")
            self.tag.full_clean()
            self.tag.save()

        self.assertEqual(tag_count, catalog.models.Tag.objects.count())

    @parameterized.parameterized.expand([("a" * 150,), ("b" * 58)])
    def test_create_tag_correct_name(self, name):
        tag_count = catalog.models.Tag.objects.count()
        self.tag = catalog.models.Tag(name=name, slug="some-correct-slug")
        self.tag.full_clean()
        self.tag.save()

        self.assertEqual(tag_count + 1, catalog.models.Tag.objects.count())

    @parameterized.parameterized.expand(
        [("s" * 201,), ("f" * 300,), ("s0me_b@d slug",), ("s%233 ",)],
    )
    def test_create_tag_unable_slug(self, slug):
        tag_count = catalog.models.Tag.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.tag = catalog.models.Tag(name="aaa", slug=slug)
            self.tag.full_clean()
            self.tag.save()

        self.assertEqual(tag_count, catalog.models.Tag.objects.count())

    def test_create_tag_with_duplicated_slug(self):
        tag_count = catalog.models.Tag.objects.count()
        self.tag = catalog.models.Tag(name="test", slug="good-slug")
        self.tag.full_clean()
        self.tag.save()

        with self.assertRaises(django.core.exceptions.ValidationError):
            self.tag1 = catalog.models.Tag(name="test name", slug="good-slug")
            self.tag1.full_clean()
            self.tag1.save()

        self.assertEqual(tag_count + 1, catalog.models.Tag.objects.count())

    @parameterized.parameterized.expand(
        [("good-slug",), ("good_slug-example")],
    )
    def test_create_tag_correct_slug(self, slug):
        tag_count = catalog.models.Tag.objects.count()
        self.tag = catalog.models.Tag(name="name", slug=slug)
        self.tag.full_clean()
        self.tag.save()

        self.assertEqual(tag_count + 1, catalog.models.Tag.objects.count())

    @parameterized.parameterized.expand(
        [("новый тег", "нoвый тeг"), ("ТЕЕГ111", "TEЕг 111")],
    )
    def test_create_tags_with_similar_normalized_names(self, name1, name2):
        self.tag = catalog.models.Tag(name=name1, slug="slug1")
        self.tag.full_clean()
        self.tag.save()

        tag_count = catalog.models.Tag.objects.count()

        with self.assertRaises(django.core.exceptions.ValidationError):
            self.tag1 = catalog.models.Tag(name=name2, slug="slug2")
            self.tag1.full_clean()
            self.tag1.save()

        self.assertEqual(tag_count, catalog.models.Tag.objects.count())
