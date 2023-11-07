import django.http
import django.shortcuts

import catalog.models
import homepage.forms


__all__ = []


def home(request):
    template = "homepage/home.html"
    items = catalog.models.Item.objects.on_main()
    context = {
        "items": items,
    }
    return django.shortcuts.render(request, template, context)


def coffee(request):
    return django.http.HttpResponse("Я чайник", status=418)


def echo(request):
    if request.method == "GET":
        template = "homepage/echo.html"
        form = homepage.forms.EchoForm()
        context = {
            "form": form,
        }
        return django.shortcuts.render(request, template, context)
    return django.http.HttpResponseNotAllowed(["POST"])


def echo_submit(request):
    if request.method == "POST":
        form = homepage.forms.EchoForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data["text"]
            return django.http.HttpResponse(
                text,
                content_type="text/plain; charset=utf-8",
                charset="utf-8",
            )
    return django.http.HttpResponseNotAllowed(["POST"])
