import os
import mimetypes

from django.http import HttpResponseNotFound
from ranged_response import RangedFileResponse
from django.conf import settings


def video_stream(request, video_file):
    _file = settings.DOWNLOAD_PATH + video_file
    if not os.path.isfile(_file):
        return HttpResponseNotFound()
    response = RangedFileResponse(
        request, open(_file, 'rb'),
        content_type=mimetypes.guess_type(_file)[0]
    )
    response['Content-Length'] = os.path.getsize(_file)
    return response


def video_download(request, video_file):
    _file = settings.DOWNLOAD_PATH + video_file
    if not os.path.isfile(_file):
        return HttpResponseNotFound()
    response = RangedFileResponse(
        request, open(_file, 'rb'),
        content_type=mimetypes.guess_type(_file)[0]
    )
    response['Content-Length'] = os.path.getsize(_file)
    response['Content-Disposition'] = 'attachment; filename="%s"' % video_file
    return response


def serve_media(request, path):
    _file = settings.MEDIA_ROOT + path
    if not os.path.isfile(_file):
        return HttpResponseNotFound()
    response = RangedFileResponse(
        request, open(_file, 'rb'),
        content_type=mimetypes.guess_type(_file)[0]
    )
    response['Content-Length'] = os.path.getsize(_file)
    return response
