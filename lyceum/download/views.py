import pathlib

import django.conf
import django.http
import django.shortcuts


__all__ = []


def download(request, img_path):
    media_path = pathlib.Path(django.conf.settings.MEDIA_ROOT)
    img_path_lib = pathlib.Path(img_path)
    file_path = pathlib.Path(media_path / img_path_lib)
    if file_path.exists():
        with file_path.open("rb") as img:
            response = django.http.HttpResponse(
                img.read(),
                content_type="application/adminupload",
            )
            response["Content-Disposition"] = (
                "inline;filename=" + img_path_lib.name
            )
            return response
    raise django.http.Http404
