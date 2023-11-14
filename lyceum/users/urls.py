import django.contrib.auth.views
import django.urls

import users.views


app_name = "users"

urlpatterns = [
    django.urls.path(
        "activate/<str:token>/",
        users.views.activate_user,
        name="activate",
    ),
    django.urls.path(
        "user_list/",
        users.views.user_list,
        name="user_list",
    ),
    django.urls.path(
        "user_detail/<int:pk>/",
        users.views.user_detail,
        name="user_detail",
    ),
    django.urls.path(
        "profile/",
        users.views.profile,
        name="profile",
    ),
    django.urls.path(
        "login/",
        django.contrib.auth.views.LoginView.as_view(
            template_name="users/login.html",
        ),
        name="login",
    ),
    django.urls.path(
        "logout/",
        django.contrib.auth.views.LogoutView.as_view(
            template_name="users/logout.html",
        ),
        name="logout",
    ),
    django.urls.path(
        "password_change/",
        django.contrib.auth.views.PasswordChangeView.as_view(
            template_name="users/password_change.html",
        ),
        name="password_change",
    ),
    django.urls.path(
        "password_change/done/",
        django.contrib.auth.views.PasswordChangeDoneView.as_view(
            template_name="users/password_change_done.html",
        ),
        name="password_change_done",
    ),
    django.urls.path(
        "password_reset/",
        django.contrib.auth.views.PasswordResetView.as_view(
            template_name="users/password_reset.html",
        ),
        name="password_reset",
    ),
    django.urls.path(
        "password_reset/done/",
        django.contrib.auth.views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    django.urls.path(
        "password_reset/confirm/",
        django.contrib.auth.views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html",
        ),
        name="password_reset_confirm",
    ),
    django.urls.path(
        "password_reset/complete/",
        django.contrib.auth.views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
    django.urls.path(
        "signup/",
        users.views.signup,
        name="signup",
    ),
]
