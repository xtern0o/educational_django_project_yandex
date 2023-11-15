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

        fields = [
            django.contrib.auth.models.User.username.field.name,
            django.contrib.auth.models.User.email.field.name,
        ]


class ProfileEditForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[
            users.models.Profile.coffee_count.field.name
        ].disabled = True
        self.fields[
            users.models.Profile.birthday.field.name
        ].widget = django.forms.fields.TextInput(
            {
                "type": "date",
            },
        )

    class Meta:
        model = users.models.Profile

        fields = [
            users.models.Profile.birthday.field.name,
            users.models.Profile.image.field.name,
            users.models.Profile.coffee_count.field.name,
        ]


class UserEditForm(django.contrib.auth.forms.UserChangeForm):
    password = None

    class Meta(django.contrib.auth.forms.UserChangeForm.Meta):
        model = users.models.ProxyUser

        fields = [
            django.contrib.auth.models.User.first_name.field.name,
            django.contrib.auth.models.User.last_name.field.name,
            django.contrib.auth.models.User.email.field.name,
        ]
