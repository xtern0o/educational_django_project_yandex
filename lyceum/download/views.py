import os

import django.conf
import django.http
import django.shortcuts


__all__ = []


def download(request, img_path):
    file_path = os.path.join(django.conf.settings.MEDIA_ROOT, img_path)
    if os.path.exists(file_path):
        with open(file_path, "rb") as img:
            response = django.http.HttpResponse(
                img.read(),
                content_type="application/adminupload",
            )
            response[
                "Content-Disposition"
            ] = "inline;filename=" + os.path.basename(img_path)
            return response
    raise django.http.Http404
