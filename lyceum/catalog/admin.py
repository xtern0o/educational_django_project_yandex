from django.contrib import admin

import catalog.models


__all__ = []


class MainImageInline(admin.TabularInline):
    model = catalog.models.MainImage


class GalleryInline(admin.TabularInline):
    model = catalog.models.Gallery
    extra = 1


@admin.register(catalog.models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        catalog.models.Item.name.field.name,
        catalog.models.Item.is_published.field.name,
        catalog.models.Item.is_on_main.field.name,
        catalog.models.Item.small_image_tmb,
    )

    list_display_links = (catalog.models.Item.name.field.name,)

    list_editable = (
        catalog.models.Item.is_published.field.name,
        catalog.models.Item.is_on_main.field.name,
    )

    filter_horizontal = (catalog.models.Item.tags.field.name,)

    readonly_fields = (catalog.models.Item.image_tmb,)

    inlines = (MainImageInline, GalleryInline)


@admin.register(catalog.models.Category)
class CategoryAdmin(admin.ModelAdmin):
    exclude = (catalog.models.Category.normalized_name.field.name,)


@admin.register(catalog.models.Tag)
class TagAdmin(admin.ModelAdmin):
    exclude = (catalog.models.Tag.normalized_name.field.name,)
