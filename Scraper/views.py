from copy import deepcopy

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect  # , HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

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


def view(request, anime_id):
    anime = get_object_or_404(AnimeResult, pk=anime_id)
    search_anime = info_handler.search(anime.name, True)
    details = info_handler.getDetailedInfo(
        search_anime[0][0]['id'])[0]
    _description = dict(details)
    del _description['id']
    del _description['image_url']
    del _description['recommendations']
    del _description['other_names']
    del _description['creators']
    # _description['description'] = str("<br>") + _description['description']
    description = dict()
    for key in _description:
        description[humanize_str(str(key))] = _description[key]
    return render(request, "Scraper/view.html", {
        "title": anime.name.title(),
        "pic_link": details['image_url'],
        "description": description,
    })
