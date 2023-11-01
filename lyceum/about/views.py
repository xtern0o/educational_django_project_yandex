import django.shortcuts


__all__ = []


def description(request):
    template = "about/description.html"
    context = {
        "title": "О проекте",
    }
    return django.shortcuts.render(request, template, context)
