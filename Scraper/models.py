import requests
import tempfile
import os

from django.db import models
from django.core import files
from django.conf import settings


class AnimeResult(models.Model):
    aid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    host = models.CharField(max_length=50)
    language = models.CharField(max_length=10)
    link = models.URLField()
    poster = models.URLField(null=True)

    def __str__(self):
        return str(self.aid) + ': ' + self.name


class Detail(models.Model):
    anime = models.OneToOneField(
        AnimeResult,
        on_delete=models.CASCADE,
        primary_key=True
    )
    poster_url = models.URLField(null=True)
    poster = models.ImageField(upload_to="images", blank=True, null=True)
    information_json = models.TextField()
    episode_last_modified = models.DateField(editable=True, null=True)

    def __str__(self):
        return str(self.anime.aid) + ": " + self.anime.name

    def save_poster_from_url(self):
        if self.poster_url:
            file_name = self.poster_url.split('/')[-1]
            directory = settings.MEDIA_ROOT + "images/"
            if not os.path.isfile(directory + file_name):
                request = requests.get(self.poster_url, stream=True)
                if request.status_code == requests.codes.ok:
                    temp_file = tempfile.NamedTemporaryFile()
                    for block in request.iter_content(1024 * 8):
                        if not block:
                            break
                        temp_file.write(block)
                    self.poster.save(file_name, files.File(temp_file))

    def poster_name(self):
        return self.poster_url.split('/')[-1]


class Episode(models.Model):
    anime = models.ForeignKey(AnimeResult, on_delete=models.CASCADE)
    episode_num = models.IntegerField()
    episode_sources_json = models.TextField()

    def __str__(self):
        return "%d: %s - Episode %d" % \
            (self.anime.aid, self.anime.name, self.episode_num)

    def getName(self):
        return "%s - Episode %d.mp4" % (self.anime.name, self.episode_num)

    def isDownloaded(self):
        if os.path.isfile(settings.DOWNLOAD_PATH + self.getName()):
            return True
        return False
