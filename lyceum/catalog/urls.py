from django.urls import path

from catalog import views


app_name = "catalog"

urlpatterns = [
    path("", views.item_list, name="item_list"),
    path("<int:pk>/", views.item_detail, name="item_detail"),
    path("new/", views.catalog_new, name="items_new"),
    path("friday/", views.catalog_changed_on_friday, name="items_friday"),
    path("unverified/", views.catalog_unverified, name="items_unverified"),
]
