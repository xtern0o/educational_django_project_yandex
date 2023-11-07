import django.db.models


__all__ = []


class FeedbackModel(django.db.models.Model):
    text = django.db.models.TextField(
        "текст",
        help_text="текст сообщения",
    )

    mail = django.db.models.EmailField(
        "e-mail",
        help_text="электронный адрес",
    )

    created_on = django.db.models.DateTimeField(
        "создано",
        auto_now_add=True,
        help_text="время создания",
    )

    class Meta:
        verbose_name = "форма обратной связи"
        verbose_name_plural = "формы обратной связи"
