from django.db import models


class AnimeResult(models.Model):
    aid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    host = models.CharField(max_length=50)
    language = models.CharField(max_length=10)
    link = models.URLField()
    poster = models.URLField(null=True)

    def __str__(self):
        return str(self.aid) + ': ' + self.name
