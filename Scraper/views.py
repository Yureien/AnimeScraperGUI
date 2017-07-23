import os
import json
import logging
from datetime import date
from threading import Thread

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseForbidden, \
    HttpResponseNotFound
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.views import View
from django.conf import settings

from .models import AnimeResult, Detail, Episode

from .anime_scrapers.scraper_handler import scraper_handler
from .anime_scrapers.info_handler import info_handler
from .anime_scrapers.download_handler import download_handler


def index(request):
    return render(request, "Scraper/index.html")


def search_page(request):
    return render(request, "Scraper/search.html")


def search(request, search_txt):
    d_results_unformatted = scraper_handler.search(search_txt)
    d_results = list()
    for a in d_results_unformatted:
        for b in a:
            d_results.append(b)
    if d_results:
        for i in d_results:
            try:
                anime = AnimeResult.objects.get(link=i['link'])
                i['aid'] = anime.aid
            except ObjectDoesNotExist:
                anime = AnimeResult(
                    name=i['title'].title(),
                    host=i['host'],
                    language=i['language'],
                    link=i['link'],
                )
                try:
                    anime.poster = i['poster']
                except KeyError:
                    anime.poster = None
                anime.save()
                i['aid'] = anime.aid
    return render(request, "Scraper/search_results.html", {
        "search_text": search_txt,
        "d_results": d_results,
    })


def login_user(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "Scraper/login.html", context={
                "error_msg": "The username/password entered is incorrect",
            })
    return render(request, "Scraper/login.html")


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return HttpResponseRedirect(reverse("index"))


def play(request, anime_id, episode_id):
    anime = get_object_or_404(AnimeResult, pk=anime_id)
    try:
        episode = anime.episode_set.get(episode_num=episode_id)
        if not episode.isDownloaded():
            return HttpResponseForbidden()
    except ObjectDoesNotExist:
        return HttpResponseNotFound()
    return render(request, "Scraper/play.html", {
        "anime_name": anime.name,
        "episode_name": episode.getName(),
        "anime_poster": anime.detail.poster_name
    })


# TODO: Create a Class.
def _download(arg):
    if not os.path.isdir(settings.DOWNLOAD_PATH):
        os.mkdir(settings.DOWNLOAD_PATH)
    successful_downloads = list()
    for x in arg:
        successful = False
        for i in x['sources']:
            logging.debug(i['link'])
            successful = download_handler.single_download(
                i['link'],
                os.path.join(settings.DOWNLOAD_PATH, x['downloadName'])
            )
            logging.debug(str(successful))
            if successful:
                break
        successful_downloads.append({
            "epNum": x['epNum'],
            "success": successful
        })
    return successful_downloads


def download(request, anime_id):
    if not anime_id:
        return HttpResponseForbidden()
    if 'd' in request.GET:
        _download_list = request.GET['d'].split(",")
        download_list = list()
        for x in _download_list:
            if x.startswith("ep-"):
                download_list.append(int(x[3:]))
            else:
                return HttpResponseForbidden()
        anime = get_object_or_404(AnimeResult, pk=anime_id)
        episodes = anime.episode_set.all()
        d_eps = list()
        for e in episodes:
            if e.episode_num in download_list:
                if not e.isDownloaded():
                    d_eps.append({
                        "epNum": e.episode_num,
                        "downloadName": e.getName(),
                        "sources": json.loads(e.episode_sources_json),
                    })
        download_thread = Thread(target=_download, args=(d_eps,))
        download_thread.start()
        msg = "Downloading episodes..." if d_eps else "Already downloaded."
        request.session['details_download_msg'] = msg
        return HttpResponseRedirect(reverse("details", args=(anime_id,)))
    return HttpResponseNotFound()


class DetailView(View):
    template_name = "Scraper/view.html"
    # Only implementing AniDB for now to get information.

    def get(self, request, anime_id):
        anime = get_object_or_404(AnimeResult, pk=anime_id)
        try:
            anime_detail = anime.detail
            details = json.loads(anime_detail.information_json)
        except ObjectDoesNotExist:
            anime_detail = Detail(anime=anime)
            search_anime = info_handler.search(anime.name, True)[0]
            if len(search_anime) > 0:
                details = info_handler.getDetailedInfo(
                    search_anime[0]['id'])[0]
                anime_detail.poster_url = details['image_url']
                if 'image_url' in details:
                    del details['image_url']
            else:
                details = {'description': 'None'}
                try:
                    anime_detail.poster_url = details['image_url']
                except:
                    anime_detail.poster_url = "None."
            anime_detail.information_json = json.dumps(details)
            anime_detail.save_poster_from_url()
            anime_detail.save()
        description = self.fix_description(dict(details))

        anime_episodes = anime.episode_set.all()
        if anime.episode_set.count() > 0 and \
           (date.today() - anime_detail.episode_last_modified)\
                .days <= settings.MAX_EPISODE_CACHE_DAYS:
            _episodes = [json.loads(ep.episode_sources_json)
                         for ep in anime_episodes]
            ep_nums = [ep.episode_num for ep in anime_episodes]
            episodes = [
                {'epNum': ep.episode_num,
                 'sources': json.loads(ep.episode_sources_json)}
                for ep in anime_episodes
            ]
        else:
            if anime.episode_set.count() > 0:
                for ep in anime.episode_set.all():
                    ep.delete()
            _episodes = scraper_handler.resolve(anime.link)['episodes']
            ep_nums = [int(x['epNum']) for x in _episodes]
            episodes = [x for (y, x) in
                        sorted(list(zip(ep_nums, _episodes)),
                               key=lambda pair: pair[0])]
            for i in sorted(ep_nums):
                anime_episode = Episode(anime=anime)
                anime_episode.episode_num = i
                anime_episode.episode_sources_json = \
                    json.dumps(episodes[i-1]['sources'])
                anime_episode.save()
            anime_detail.episode_last_modified = date.today()
            anime_detail.save()

        downloaded_eps = list()
        for ep in anime.episode_set.all():
            if ep.isDownloaded():
                downloaded_eps.append(ep.episode_num)
        info_msg = ""
        if 'details_download_msg' in request.session:
            info_msg = request.session.pop('details_download_msg')

        return render(request, self.template_name, {
            "title": anime.name.title(),
            "poster_name": anime_detail.poster_name,
            "description": description,
            "ep_nums": sorted(ep_nums),
            "downloaded_eps": downloaded_eps,
            "aid": anime_id,
            "info_message": info_msg
        })

    def fix_description(self, description):
        if 'id' in description:
            del description['id']
        if 'recommendations' in description:
            del description['recommendations']
        if 'other_names' in description:
            del description['other_names']
        if 'creators' in description:
            del description['creators']
        # description['description'] =
        # str("<br>") + description['description']
        new_description = dict()
        if len(description) > 0:
            for key in description:
                new_description[self.humanize_str(str(key))] = description[key]
        return new_description

    def humanize_str(self, string):
        string = string.replace("_", " ")
        string = string.title()
        return string
