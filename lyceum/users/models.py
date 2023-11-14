import pathlib

import django.contrib.auth.models
import django.db


__all__ = []


class UserManager(django.contrib.auth.models.UserManager):
    def get_active_users(self):
        return (
            self.get_queryset().filter(is_active=True).only("id", "username")
        )

    def get_user_detail(self, pk):
        return (
            self.get_queryset()
            .filter(pk=pk)
            .select_related("profile")
            .only(
                "first_name",
                "last_name",
                "profile__image",
                "profile__birthday",
                "profile__coffee_count",
            )
        )


class Profile(django.db.models.Model):
    def get_avatar_path(self, filename):
        return (
            pathlib.Path("users")
            / f"avatar_user_{str(self.user.id)}.{filename.split('.')[-1]}"
        )

    user = django.db.models.OneToOneField(
        django.contrib.auth.models.User,
        on_delete=django.db.models.deletion.CASCADE,
    )

    birthday = django.db.models.DateField(
        "дата рождения",
        blank=True,
        null=True,
    )

    image = django.db.models.ImageField(
        "аватарка",
        blank=True,
        null=True,
        upload_to=get_avatar_path,
    )

    coffee_count = django.db.models.PositiveIntegerField(
        "счётчик кофе",
        default=0,
    )

    class Meta:
        verbose_name = "дополнительное поле"
        verbose_name_plural = "дополнительные поля"


class ProxyUser(django.contrib.auth.models.User):
    objects = UserManager()

    class Meta:
        proxy = True