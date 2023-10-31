import django.db
import django.shortcuts

import catalog.models


__all__ = []


def item_list(request):
    template = "catalog/item_list.html"
    items = catalog.models.Item.objects.published().order_by("category__name")
    cycle_list = ["1", "2", "3"]
    context = {
        "items": items,
        "cycle_list": cycle_list,
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
