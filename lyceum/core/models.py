import re

import django.core.validators
import django.db.models
import django.utils.safestring


__all__ = []


class AbstractModelNamePublished(django.db.models.Model):
    name = django.db.models.CharField(
        "название",
        max_length=150,
        help_text="Название объекта (не более 150 символов)",
        unique=True,
    )

    is_published = django.db.models.BooleanField("опубликовано", default=True)

    class Meta:
        abstract = True


class AbstractModelSlug(django.db.models.Model):
    slug = django.db.models.SlugField(
        "слаг",
        max_length=200,
        unique=True,
        validators=[
            django.core.validators.validate_slug,
        ],
        help_text="Короткая метка для использования в URL "
        "(только латиница, цифры, подчеркивание и дефисы)",
    )

    class Meta:
        abstract = True


class AbstractModelNormalizedName(django.db.models.Model):
    normalized_name = django.db.models.CharField(
        "нормализованное имя",
        max_length=300,
        unique=True,
        default="-",
    )

    def clean(self):
        if self._normalize_name(self.name) in [
            n.normalized_name for n in type(self).objects.all()
        ]:
            raise django.core.exceptions.ValidationError(
                "Название, похожее на это уже существует",
            )
        self.normalized_name = self._normalize_name(self.name)

    def _normalize_name(self, name):
        similar_letters = {
            "а": "a",
            "в": "b",
            "е": "e",
            "к": "k",
            "м": "m",
            "н": "h",
            "о": "o",
            "р": "p",
            "с": "c",
            "т": "t",
            "у": "y",
            "х": "x",
        }

        normalized = list(re.sub(r"\s+|[^\w\s]", "", name).lower())

        for i in range(len(normalized)):
            if normalized[i] in similar_letters:
                normalized[i] = similar_letters[normalized[i]]
        normalized = "".join(normalized)

        return normalized

    class Meta:
        abstract = True


class AbstractImage(django.db.models.Model):
    image = django.db.models.ImageField(
        "изображение",
        upload_to="catalog/%Y/%m/%d/",
    )

    class Meta:
        abstract = True
