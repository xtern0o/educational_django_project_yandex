import django.db

import catalog.models


__all__ = []


class ItemManager(django.db.models.Manager):
    def published(self):
        return (
            self.get_queryset()
            .filter(is_published=True, category__is_published=True)
            .select_related("category", "mainimage")
            .prefetch_related(
                django.db.models.Prefetch(
                    "tags",
                    queryset=catalog.models.Tag.objects.published(),
                ),
            )
            .only(
                "name",
                "text",
                "category__name",
                "mainimage__image",
            )
        )


class TagManager(django.db.models.Manager):
    def published(self):
        return (
            self.get_queryset()
            .filter(is_published=True)
            .only(
                "name",
            )
        )
