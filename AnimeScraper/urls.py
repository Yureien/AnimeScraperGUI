"""AnimeScraper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('Scraper.urls')),
    url(r'^videos/(?P<video_file>[0-9a-zA-Z _!@$|:;&*()"\'.,<>+=`-]+)/$',
        views.video_stream, name='v_stream'),
    url(r'^videos/download/' +
        '(?P<video_file>[0-9a-zA-Z _!@$|:;&*()"\'.,<>+=`-]+)/$',
        views.video_download, name='v_download'),
    url(r'^' + settings.MEDIA_URL + "(?P<path>.*)$",
        views.serve_media, name='media'),
]
