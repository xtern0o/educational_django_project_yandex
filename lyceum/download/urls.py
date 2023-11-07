from django.urls import path

from download import views


app_name = "download"

urlpatterns = [
    path("<path:img_path>/", views.download, name="download_file"),
]
