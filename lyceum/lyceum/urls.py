import django.conf
import django.conf.urls.static
import django.contrib.admin
import django.contrib.auth
import django.urls


urlpatterns = [
    django.urls.path("", django.urls.include("homepage.urls")),
    django.urls.path("about/", django.urls.include("about.urls")),
    django.urls.path("catalog/", django.urls.include("catalog.urls")),
    django.urls.path("download/", django.urls.include("download.urls")),
    django.urls.path("feedback/", django.urls.include("feedback.urls")),
    django.urls.path("auth/", django.urls.include("users.urls")),
    django.urls.path(
        "auth/",
        django.urls.include("django.contrib.auth.urls"),
    ),
    django.urls.path("admin/", django.contrib.admin.site.urls),
]
urlpatterns += django.conf.urls.static.static(
    django.conf.settings.STATIC_URL,
    document_root=django.conf.settings.STATIC_ROOT,
)
urlpatterns += django.conf.urls.static.static(
    django.conf.settings.MEDIA_URL,
    document_root=django.conf.settings.MEDIA_ROOT,
)

if django.conf.settings.DEBUG:
    import debug_toolbar

    urlpatterns += (
        django.urls.path(
            "__debug__/",
            django.urls.include(debug_toolbar.urls),
        ),
    )
