import datetime

import django.conf
import django.contrib.auth
import django.contrib.auth.decorators
import django.contrib.auth.models
import django.core.mail
import django.shortcuts
import django.urls
import django.utils.timezone
import jwt

import core.utils
import users.forms
import users.models


__all__ = []


def signup(request):
    template = "users/signup.html"
    form = users.forms.SignUpForm(request.POST or None)
    context = {
        "form": form,
    }
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            users.models.Profile.objects.create(
                user=user,
            )

            if django.conf.settings.DEFAULT_USER_IS_ACTIVE:
                user.is_active = True
                user.save()

            expiration = django.utils.timezone.now() + datetime.timedelta(
                hours=django.conf.settings.LINK_EXPIRATION,
            )

            exp_timestamp = int(expiration.timestamp())

            token_context = {
                "username": user.username,
                "exp": exp_timestamp,
            }

            token = jwt.encode(
                token_context,
                django.conf.settings.SECRET_KEY,
                algorithm="HS256",
            )

            activation_link = request.build_absolute_uri(
                django.urls.reverse(
                    "users:activate",
                    kwargs={
                        "token": token,
                    },
                ),
            )

            msg_text = (
                f"Вам необходимо активировать аккаунт в течение 12 "
                "часов после регистрации. "
                "Для активации перейдите по ссылке, указанной в"
                " данном письме.\n"
                f"Ссылка для активации: {activation_link}"
            )

            django.core.mail.send_mail(
                "Активация аккаунта",
                msg_text,
                django.conf.settings.EMAIL_ADDRESS,
                [user.email],
            )

            django.contrib.auth.login(
                request,
                user,
                backend="users.backends.LoginBackend",
            )
            return django.shortcuts.redirect(
                django.urls.reverse("homepage:home"),
            )
    return django.shortcuts.render(request, template, context)


def activate_user(request, token):
    template = "users/activation_success.html"
    data, status_ok = core.utils.decode_token(token)

    if status_ok:
        user = django.contrib.auth.models.User.objects.get(
            username=data["username"],
        )
        user.is_active = True
        user.save()

        context = {
            "info": "Аккаунт успешно активирован",
            "ok": status_ok,
        }

    else:
        context = {
            "info": data,
            "ok": status_ok,
        }

    return django.shortcuts.render(request, template, context)


def user_list(request):
    template = "users/user_list.html"
    active_users = users.models.ProxyUser.objects.active().all()
    context = {
        "users": active_users,
    }
    return django.shortcuts.render(request, template, context)


def user_detail(request, pk):
    template = "users/user_detail.html"
    user = django.shortcuts.get_object_or_404(
        users.models.ProxyUser.objects.get_user_detail(pk),
    )
    context = {
        "user": user,
    }
    return django.shortcuts.render(request, template, context)


@django.contrib.auth.decorators.login_required
def profile(request):
    template = "users/profile.html"
    user = request.user

    user_form = users.forms.UserEditForm(
        request.POST or None,
        initial={
            "first_name": user.first_name if user.first_name else "",
            "last_name": user.last_name if user.last_name else "",
            "username": user.username,
            "email": user.email,
        },
        instance=user,
    )

    birthday = user.profile.birthday
    if user.profile.birthday:
        user.profile.birthday.isoformat()

    profile_form = users.forms.ProfileEditForm(
        request.POST or None,
        request.FILES or None,
        initial={
            "image": user.profile.image,
            "birthday": birthday,
        },
        instance=user.profile,
    )

    if user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile_form.save()
        return django.shortcuts.redirect("users:profile")

    if not user.is_authenticated:
        return django.shortcuts.redirect("users:login")

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
        "coffee_count": user.profile.coffee_count,
    }
    return django.shortcuts.render(request, template, context)
