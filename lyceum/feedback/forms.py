import django.core.validators
import django.forms

import feedback.models


__all__ = []


class FeedbackForm(django.forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control my-1"
            field.field.widget.attrs["placeholder"] = field.field.label

    text = django.forms.CharField(
        label="Ваш текст",
        help_text="Ваши впечатления, вопросы",
        widget=django.forms.Textarea,
    )

    mail = django.forms.EmailField(
        label="Почта",
        help_text="Ваш электронный адрес",
        validators=[
            django.core.validators.EmailValidator(
                message="Некорректный e-mail адрес",
            ),
        ],
    )

    class Meta:
        model = feedback.models.FeedbackModel
        exclude = ["text", "mail", "created_on"]
