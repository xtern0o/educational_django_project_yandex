import datetime

import django.db
import django.shortcuts
import django.utils.timezone

import catalog.models


__all__ = []


def item_list(request):
    template = "catalog/item_list.html"
    items = catalog.models.Item.objects.published().order_by("category__name")
    context = {
        "items": items,
    }
    return django.shortcuts.render(request, template, context)


def item_detail(request, pk):
    template = "catalog/item_detail.html"
    item = django.shortcuts.get_object_or_404(
        catalog.models.Item.objects.filter(is_published=True)
        .prefetch_related(
            django.db.models.Prefetch(
                "tags",
                queryset=catalog.models.Tag.objects.published(),
            ),
        )
        .only("name", "text", "main_image", "category__name"),
        pk=pk,
    )
    context = {
        "item": item,
    }
    return django.shortcuts.render(request, template, context)


def catalog_new(request):
    template = "catalog/item_list.html"
    end_date = django.utils.timezone.now()
    start_date = end_date - datetime.timedelta(days=7)
    items = (
        catalog.models.Item.objects.published()
        .filter(
            created_at__range=[
                start_date,
                end_date,
            ],
        )
        .order_by("?")
    )[:5]
    items = sorted(items, key=lambda item: item.category.name)
    # да, возможно костыли, но зато без использования regroup...
    context = {
        "items": items,
    }
    return django.shortcuts.render(request, template, context)


def catalog_changed_on_friday(request):
    template = "catalog/item_list.html"
    items = (
        catalog.models.Item.objects.published().filter(
            updated_at__week_day=6,
        )
    )[:5]
    context = {
        "items": items,
    }
    return django.shortcuts.render(request, template, context)


def catalog_unverified(request):
    template = "catalog/item_list.html"
    # Сравниваю через разницу в 200мс, так как 2 поля
    # заполняются не одновременно
    items = (
        catalog.models.Item.objects.published()
        .annotate(
            time_diff=django.db.models.ExpressionWrapper(
                django.db.models.F("updated_at")
                - django.db.models.F(
                    "created_at",
                ),
                output_field=django.db.models.DurationField(),
            ),
        )
        .filter(
            time_diff__lte=datetime.timedelta(milliseconds=200),
        )
    )
    context = {
        "items": items,
    }
    return django.shortcuts.render(request, template, context)
