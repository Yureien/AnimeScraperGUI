from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect  # , HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.views import View

from .models import AnimeResult

from .anime_scrapers.scraper_handler import scraper_handler
from .anime_scrapers.info_handler import info_handler


def index(request):
    return render(request, "Scraper/index.html")


def search_page(request):
    return render(request, "Scraper/search.html")


def search(request, search_txt):
    d_results = list()
    # i_results = list() TODO: WIP.
    search_result_types = list()
    if request.GET:
        if 'i' in request.GET:
            search_result_types.append("Information Search")
        if 'd' in request.GET:
            d_results_unformatted = scraper_handler.search(search_txt)
            for a in d_results_unformatted:
                for b in a:
                    d_results.append(b)
            search_result_types.append("Download Search")
    else:
        d_results_unformatted = scraper_handler.search(search_txt)
        for a in d_results_unformatted:
            for b in a:
                d_results.append(b)
        search_result_types.append("Information Search")
        search_result_types.append("Download Search")
    if d_results:
        for i in d_results:
            try:
                anime = AnimeResult.objects.get(link=i['link'])
                i['aid'] = anime.aid
            except ObjectDoesNotExist:
                anime = AnimeResult(
                    name=i['title'],
                    host=i['host'],
                    language=i['language'],
                    link=i['link'],
                )
                try:
                    anime.poster = i['poster']
                except KeyError:
                    anime.poster = None
                i['aid'] = anime.aid
                anime.save()
    return render(request, "Scraper/search_results.html", {
        "search_text": search_txt,
        "i_results": d_results,  # TODO: WIP.
        "d_results": d_results,
        "results_loop": search_result_types,
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


def humanize_str(string):
    string = string.replace("_", " ")
    string = string.title()
    return string


class DetailView(View):
    template_name = "Scraper/view.html"
    # Only implementing AniDB for now to get information.

    def get(self, request, anime_id):
        anime = get_object_or_404(AnimeResult, pk=anime_id)
        search_anime = info_handler.search(anime.name, True)[0]
        if len(search_anime) <= 0:
            search_anime = info_handler.search(anime.name, False)[0]
            aid = self.find_most_similar(anime.name, search_anime)
            details = info_handler.getDetailedInfo(aid)[0]
        else:
            details = {'description': 'None'}
            try:
                details['image_url'] = anime.poster
            except:
                details['image_url'] = "None lol. Idk why."
        description = self.fix_description(dict(details))
        anime_details = scraper_handler.resolve(anime.link)
        episodes = list()
        _last_id = -1
        for x in anime_details['episodes']:
            if _last_id == -1:
                _last_id = x['epNum']
                episodes.append(x)
            else:
                _id = x['epNum']
                if _id > _last_id:
                    episodes.append(x)
                else:
                    episodes.insert(0, x)
                _last_id = _id
        return render(request, "Scraper/view.html", {
            "title": anime.name.title(),
            "pic_link": details['image_url'],
            "description": description,
            "debug_txt": [x['epNum'] for x in episodes]
        })

    def fix_description(self, description):
        if 'id' in description:
            del description['id']
        if 'image_url' in description:
            del description['image_url']
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
                new_description[humanize_str(str(key))] = description[key]
        return new_description
