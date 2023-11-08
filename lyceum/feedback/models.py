import django.conf
import django.db.models


__all__ = []


class Feedback(django.db.models.Model):
    class StatusChoices(django.db.models.TextChoices):
        GOT = ("GT", "получено")
        IN_POCESSING = ("PR", "в обработке")
        DONE = ("OK", "ответ дан")

    name = django.db.models.TextField(
        "имя отправителя",
        help_text="имя указанное как автор при отправлении",
        null=True,
        blank=True,
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
        to=django.conf.settings.AUTH_USER_MODEL,
        on_delete=django.db.models.CASCADE,
        related_name="user",
        help_text="пользователь",
        related_query_name="user",
    )

    feedback = django.db.models.ForeignKey(
        to=Feedback,
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
