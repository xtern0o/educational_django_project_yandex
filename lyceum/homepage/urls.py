from django.urls import path

from . import views


app_name = "homepage"

urlpatterns = [
    path("", views.home, name="home"),
    path("coffee/", views.coffee, name="coffee"),
]
