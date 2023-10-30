# Generated by Django 4.2 on 2023-10-23 18:35

import catalog.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0002_alter_category_normalized_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="name",
            field=models.CharField(
                help_text="Название объекта (не более 150 символов)",
                max_length=150,
                unique=True,
                verbose_name="название",
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="slug",
            field=models.SlugField(
                help_text="Короткая метка для использования в URL (только латиница, цифры, подчеркивание и дефисы)",
                max_length=200,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        re.compile("^[-a-zA-Z0-9_]+\\Z"),
                        "Enter a valid “slug” consisting of letters, numbers, underscores or hyphens.",
                        "invalid",
                    )
                ],
                verbose_name="слаг",
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="weight",
            field=models.IntegerField(
                default=100,
                help_text="Вес (от 1 до 32767 включительно)",
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(32767),
                ],
                verbose_name="вес",
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="category",
            field=models.ForeignKey(
                help_text="Категория товара",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="catalog_name",
                to="catalog.category",
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="name",
            field=models.CharField(
                help_text="Название объекта (не более 150 символов)",
                max_length=150,
                unique=True,
                verbose_name="название",
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="tags",
            field=models.ManyToManyField(help_text="Тег", to="catalog.tag"),
        ),
        migrations.AlterField(
            model_name="item",
            name="text",
            field=models.TextField(
                help_text="Описание товара",
                validators=[
                    catalog.validators.ValidateMustContain(
                        "превосходно", "роскошно"
                    )
                ],
                verbose_name="текст",
            ),
        ),
        migrations.AlterField(
            model_name="tag",
            name="name",
            field=models.CharField(
                help_text="Название объекта (не более 150 символов)",
                max_length=150,
                unique=True,
                verbose_name="название",
            ),
        ),
        migrations.AlterField(
            model_name="tag",
            name="slug",
            field=models.SlugField(
                help_text="Короткая метка для использования в URL (только латиница, цифры, подчеркивание и дефисы)",
                max_length=200,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        re.compile("^[-a-zA-Z0-9_]+\\Z"),
                        "Enter a valid “slug” consisting of letters, numbers, underscores or hyphens.",
                        "invalid",
                    )
                ],
                verbose_name="слаг",
            ),
        ),
        migrations.CreateModel(
            name="Image",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        upload_to="catalog/% Y/% m/% d/",
                        verbose_name="изображение",
                    ),
                ),
                (
                    "item",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="main_image",
                        to="catalog.item",
                        verbose_name="товар",
                    ),
                ),
            ],
            options={
                "verbose_name": "изобравжение",
                "verbose_name_plural": "изображения",
            },
        ),
        migrations.CreateModel(
            name="Gallery",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        upload_to="catalog/% Y/% m/% d/",
                        verbose_name="изображение",
                    ),
                ),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="gallery",
                        to="catalog.item",
                        verbose_name="товар",
                    ),
                ),
            ],
            options={
                "verbose_name": "галерея",
                "verbose_name_plural": "галереи",
            },
        ),
    ]
