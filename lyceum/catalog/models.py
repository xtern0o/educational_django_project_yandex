import ckeditor.fields
import django.core.exceptions
import django.core.validators
import django.db
import django.urls
import django.utils.safestring
import sorl.thumbnail

import catalog.validators
import core.models


__all__ = []


class ItemManager(django.db.models.Manager):
    def published(self):
        return (
            self.get_queryset()
            .filter(is_published=True, category__is_published=True)
            .select_related("category", "main_image")
            .prefetch_related(
                django.db.models.Prefetch(
                    "tags",
                    queryset=Tag.objects.published(),
                ),
            )
            .only(
                "name",
                "text",
                "category__name",
                "main_image__image",
            )
        )

    def on_main(self):
        return self.published().filter(is_on_main=True).order_by("name")


class TagManager(django.db.models.Manager):
    def published(self):
        return self.get_queryset().filter(is_published=True).only("name")


class Item(core.models.AbstractModelNamePublished):
    objects = ItemManager()

    text = ckeditor.fields.RichTextField(
        "текст",
        validators=[
            catalog.validators.ValidateMustContain(
                "превосходно",
                "роскошно",
            ),
        ],
        help_text="Описание товара"
        " (должно содержать слово превосходно или роскошно)",
    )

    is_on_main = django.db.models.BooleanField(
        "на главной странице",
        default=False,
        help_text="Отображать ли товар на главной странице?",
    )

    category = django.db.models.ForeignKey(
        "catalog.Category",
        on_delete=django.db.models.CASCADE,
        related_name="category",
        help_text="Категория товара",
        related_query_name="category",
    )

    tags = django.db.models.ManyToManyField("catalog.Tag", help_text="Тег")

    created_at = django.db.models.DateTimeField(
        "время создания",
        auto_now_add=True,
    )
    updated_at = django.db.models.DateTimeField(
        "время последнего изменения",
        auto_now=True,
    )

    class Meta:
        ordering = ("name", "id")
        verbose_name = "товар"
        verbose_name_plural = "товары"

    def __str__(self):
        return self.name[:15]

    def get_image_x300(self):
        return sorl.thumbnail.get_thumbnail(
            self.main_image.image,
            "300x300",
            crop="center",
            quality=51,
        )

    def get_image_x50(self):
        return sorl.thumbnail.get_thumbnail(
            self.main_image.image,
            "50x50",
            crop="center",
            quality=51,
        )

    def image_tmb(self):
        if self.main_image:
            return django.utils.safestring.mark_safe(
                f'<img src="{self.get_image_x300().url}">',
            )
        return "изображения нет"

    image_tmb.short_description = "превью (300x300)"
    image_tmb.allow_tags = True

    def small_image_tmb(self):
        if self.main_image:
            return django.utils.safestring.mark_safe(
                f'<img src="{self.get_image_x50().url}">',
            )
        return "изображения нет"

    small_image_tmb.short_description = "превью (50x50)"
    small_image_tmb.allow_tags = True


class Tag(
    core.models.AbstractModelNamePublished,
    core.models.AbstractModelNormalizedName,
    core.models.AbstractModelSlug,
):
    objects = TagManager()

    class Meta:
        ordering = ("name", "id")
        verbose_name = "тег"
        verbose_name_plural = "теги"

    def __str__(self):
        return self.name[:15]


class Category(
    core.models.AbstractModelNamePublished,
    core.models.AbstractModelNormalizedName,
    core.models.AbstractModelSlug,
):
    weight = django.db.models.IntegerField(
        "вес",
        default=100,
        validators=[
            django.core.validators.MinValueValidator(1),
            django.core.validators.MaxValueValidator(32767),
        ],
        help_text="Вес (от 1 до 32767 включительно)",
    )

    class Meta:
        ordering = ("name", "id")
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return self.name[:15]


class MainImage(core.models.AbstractImage):
    item = django.db.models.OneToOneField(
        "catalog.Item",
        verbose_name="товар",
        on_delete=django.db.models.deletion.CASCADE,
        null=True,
        related_name="main_image",
    )

    class Meta:
        verbose_name = "главное изображение"
        verbose_name_plural = "главные изображения"


class Gallery(core.models.AbstractImage):
    item = django.db.models.ForeignKey(
        "catalog.Item",
        verbose_name="товар",
        on_delete=django.db.models.deletion.CASCADE,
        related_name="images",
        related_query_name="image",
    )

    class Meta:
        verbose_name = "дополнительное изображение"
        verbose_name_plural = "галерея"
