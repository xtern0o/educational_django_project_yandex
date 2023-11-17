import django.db.models.query
import django.test
import django.urls
import django.utils.timezone
import freezegun
import parameterized

import catalog.models


__all__ = []


class ContextTests(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        with freezegun.freeze_time("01-01-2023"):
            cls.published_category = catalog.models.Category(
                is_published=True,
                name="Published category",
                slug="pub-cat",
            )
            cls.unpublished_category = catalog.models.Category(
                is_published=False,
                name="Unpublished category",
                slug="unpub-cat",
            )

            cls.published_tag = catalog.models.Tag(
                is_published=True,
                name="Published tag",
                slug="pub-tag",
            )
            cls.unpublished_tag = catalog.models.Tag(
                is_published=True,
                name="Unpublished tag",
                slug="unpub-tag",
            )

            cls.published_category.clean()
            cls.unpublished_category.clean()
            cls.published_tag.clean()
            cls.unpublished_tag.clean()

            cls.published_category.save()
            cls.unpublished_category.save()
            cls.published_tag.save()
            cls.unpublished_tag.save()

            cls.published_item = catalog.models.Item(
                name="Published item",
                category=cls.published_category,
                text="роскошно",
            )

            cls.published_item_on_main = catalog.models.Item(
                name="Published on main item",
                category=cls.published_category,
                text="роскошно",
                is_on_main=True,
            )
            cls.unpublished_item = catalog.models.Item(
                name="Unpublished item",
                category=cls.unpublished_category,
                text="роскошно",
            )
            cls.unpublished_item_on_main = catalog.models.Item(
                name="Unpublished on main item",
                category=cls.unpublished_category,
                text="роскошно",
                is_on_main=True,
            )

            cls.published_item.clean()
            cls.published_item_on_main.clean()
            cls.unpublished_item.clean()
            cls.unpublished_item_on_main.clean()

            cls.published_item.save()
            cls.published_item_on_main.save()
            cls.unpublished_item.save()
            cls.unpublished_item_on_main.save()

            cls.published_item.tags.add(cls.published_tag)
            cls.published_item_on_main.tags.add(cls.published_tag)
            cls.unpublished_item.tags.add(cls.unpublished_tag)
            cls.unpublished_item_on_main.tags.add(cls.unpublished_tag)

        with freezegun.freeze_time("01-06-2023"):
            cls.published_item_friday = catalog.models.Item(
                name="Published item Friday",
                category=cls.published_category,
                text="роскошно fd",
            )
            cls.published_item_friday.clean()
            cls.published_item_friday.save()
            cls.published_item_friday.tags.add(cls.published_tag)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.published_category.delete()
        cls.unpublished_category.delete()
        cls.published_tag.delete()
        cls.unpublished_tag.delete()
        cls.published_item.delete()
        cls.published_item_on_main.delete()
        cls.unpublished_item.delete()
        cls.published_item_friday.delete()

    @parameterized.parameterized.expand(
        [
            ("homepage:home",),
            ("catalog:item_list",),
        ],
    )
    def test_type_of_context(self, app_url):
        response = django.test.Client().get(
            django.urls.reverse(app_url),
        )
        items = response.context["items"]
        self.assertIsInstance(items, django.db.models.query.QuerySet)

    @parameterized.parameterized.expand(
        [
            ("homepage:home",),
            ("catalog:item_list",),
        ],
    )
    def test_correct_context(self, app_url):
        response = django.test.Client().get(
            django.urls.reverse(app_url),
        )
        self.assertIn("items", response.context)

    @parameterized.parameterized.expand(
        [
            ("homepage:home", 1),
            ("catalog:item_list", 3),
        ],
    )
    def test_published_item_count(self, app_url, correct_count):
        response = django.test.Client().get(
            django.urls.reverse(app_url),
        )
        items = response.context["items"]
        self.assertEqual(len(items), correct_count)

    @parameterized.parameterized.expand(
        [
            ("homepage:home"),
            ("catalog:item_list"),
        ],
    )
    def test_excluding_bad_attributes_in_querysets(self, app_url):
        response = django.test.Client().get(
            django.urls.reverse(app_url),
        )
        items = response.context["items"]
        item_attributes = items[0].__dict__
        tag_attributes = item_attributes["_prefetched_objects_cache"]["tags"][
            0
        ].__dict__
        self.assertNotIn("is_published", item_attributes)
        self.assertNotIn("images", item_attributes)
        self.assertNotIn("is_published", tag_attributes)

    def test_context_new(self):
        response = django.test.Client().get(
            django.urls.reverse("catalog:items_new"),
        )
        items = response.context["items"]
        self.assertEqual(len(items), 0)

    def test_context_friday(self):
        response = django.test.Client().get(
            django.urls.reverse("catalog:items_friday"),
        )
        items = response.context["items"]
        self.assertEqual(len(items), 1)

    def test_context_unverified(self):
        response = django.test.Client().get(
            django.urls.reverse("catalog:items_unverified"),
        )
        items = response.context["items"]
        self.assertEqual(len(items), 3)
