# Generated by Django 4.2 on 2023-11-08 16:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    replaces = [
        ("feedback", "0001_initial"),
        ("feedback", "0002_feedbackmodel_name"),
        ("feedback", "0003_feedbackmodel_status"),
        ("feedback", "0004_alter_feedbackmodel_status_statuslog"),
        ("feedback", "0005_statuslog_feedback"),
        ("feedback", "0006_alter_statuslog_feedback"),
    ]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="FeedbackModel",
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
                    "text",
                    models.TextField(
                        help_text="текст сообщения", verbose_name="текст"
                    ),
                ),
                (
                    "mail",
                    models.EmailField(
                        help_text="электронный адрес",
                        max_length=254,
                        verbose_name="e-mail",
                    ),
                ),
                (
                    "created_on",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="время создания",
                        verbose_name="создано",
                    ),
                ),
                (
                    "name",
                    models.TextField(
                        default="ANONYMOUS",
                        help_text="имя указанное как автор при отправлении",
                        verbose_name="имя отправителя",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("GT", "получено"),
                            ("PR", "в обработке"),
                            ("OK", "ответ дан"),
                        ],
                        default="GT",
                        help_text="статус обработки формы",
                        max_length=2,
                        verbose_name="статус обработки",
                    ),
                ),
            ],
            options={
                "verbose_name": "форма обратной связи",
                "verbose_name_plural": "формы обратной связи",
            },
        ),
        migrations.CreateModel(
            name="StatusLog",
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
                    "timestamp",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="время создания"
                    ),
                ),
                (
                    "from_status",
                    models.CharField(
                        db_column="from",
                        max_length=2,
                        verbose_name="начальное состояние",
                    ),
                ),
                (
                    "to",
                    models.CharField(
                        max_length=2, verbose_name="новое состояние"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        help_text="пользователь",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user",
                        related_query_name="user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "feedback",
                    models.ForeignKey(
                        help_text="фидбек",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="feedback",
                        related_query_name="feedback",
                        to="feedback.feedbackmodel",
                    ),
                ),
            ],
            options={
                "verbose_name": "лог статусов",
                "verbose_name_plural": "логи статусов",
            },
        ),
    ]
