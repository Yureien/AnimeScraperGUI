import logging
import glob
import os

from django.apps import AppConfig
from django.conf import settings


class ScraperConfig(AppConfig):
    name = 'Scraper'

    def ready(self):
        download_path = settings.DOWNLOAD_PATH
        cur_dir = os.getcwd()
        os.chdir(download_path)
        for f in glob.glob("*.tmp"):
            logging.debug("Removing file: %s" % (f))
            os.remove(f)
        os.chdir(cur_dir)
