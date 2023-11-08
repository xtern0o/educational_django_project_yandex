import django.contrib.auth.models
import django.db.models


__all__ = []

User = django.contrib.auth.get_user_model()


class FeedbackModel(django.db.models.Model):
    class StatusChoices(django.db.models.TextChoices):
        GOT = "GT", "получено"
        IN_POCESSING = "PR", "в обработке"
        DONE = "OK", "ответ дан"

    name = django.db.models.TextField(
        "имя отправителя",
        help_text="имя указанное как автор при отправлении",
        default="ANONYMOUS",
    )

    text = django.db.models.TextField(
        "текст",
        help_text="текст сообщения",
    )

    mail = django.db.models.EmailField(
        "e-mail",
        help_text="электронный адрес",
    )

    status = django.db.models.CharField(
        "статус обработки",
        max_length=2,
        help_text="статус обработки формы",
        choices=StatusChoices.choices,
        default=StatusChoices.GOT,
    )

    created_on = django.db.models.DateTimeField(
        "создано",
        auto_now_add=True,
        help_text="время создания",
    )

    def clean(self):
        super().clean()

    class Meta:
        verbose_name = "форма обратной связи"
        verbose_name_plural = "формы обратной связи"


class StatusLog(django.db.models.Model):
    user = django.db.models.ForeignKey(
        to=User,
        on_delete=django.db.models.CASCADE,
        related_name="user",
        help_text="пользователь",
        related_query_name="user",
    )

    feedback = django.db.models.ForeignKey(
        to=FeedbackModel,
        on_delete=django.db.models.CASCADE,
        related_name="feedback",
        related_query_name="feedback",
        help_text="фидбек",
    )

    timestamp = django.db.models.DateTimeField(
        "время создания",
        auto_now_add=True,
    )

    from_status = django.db.models.CharField(
        "начальное состояние",
        max_length=2,
        db_column="from",
    )

    to = django.db.models.CharField(
        "новое состояние",
        max_length=2,
    )

    class Meta:
        verbose_name = "лог статусов"
        verbose_name_plural = "логи статусов"
