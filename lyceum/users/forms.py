import django.contrib.auth.forms
import django.contrib.auth.models
import django.forms
import django.forms.fields

import users.models


__all__ = []


class SignUpForm(django.contrib.auth.forms.UserCreationForm):
    email = django.forms.EmailField(
        required=True,
    )

    class Meta:
        model = django.contrib.auth.models.User
        fields = (
            django.contrib.auth.models.User.username.field.name,
            django.contrib.auth.models.User.email.field.name,
        )


class ProfileEditForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[
            users.models.Profile.birthday.field.name
        ].widget = django.forms.fields.TextInput(
            {
                "type": "date",
            },
        )

    class Meta:
        model = users.models.Profile
        fields = (
            users.models.Profile.birthday.field.name,
            users.models.Profile.image.field.name,
        )


class UserEditForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = users.models.ProxyUser
        fields = (
            users.models.ProxyUser.first_name.field.name,
            users.models.ProxyUser.last_name.field.name,
            users.models.ProxyUser.email.field.name,
        )
