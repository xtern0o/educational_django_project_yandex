import django.shortcuts

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
        catalog.models.Item.objects.filter(is_published=True),
        pk=pk,
    )
    context = {
        "item": item,
    }
    return django.shortcuts.render(request, template, context)
