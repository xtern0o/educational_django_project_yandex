import django.http
import django.shortcuts

import catalog.models


__all__ = []


def home(request):
    template = "homepage/home.html"
    items = (
        catalog.models.Item.objects.published()
        .filter(is_on_main=True)
        .order_by("name")
    )
    context = {
        "items": items,
    }
    return django.shortcuts.render(request, template, context)


def coffee(request):
    return django.http.HttpResponse("Я чайник", status=418)
