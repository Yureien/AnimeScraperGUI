from django.shortcuts import render
from django.http import HttpResponseRedirect  # HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

import sys
sys.path.append("/home/soham/Documents/AnimeScraperGUI/Scraper/scrapers")
sys.path.append("/home/soham/Documents/AnimeScraperGUI/Scraper/scrapers/scrapers")
from scraper_handler import scraper_handler


def index(request):
    return render(request, "Scraper/index.html")


def search_page(request):
    return render(request, "Scraper/search.html")


def search(request, search_txt):
    search_types = list()
    if request.GET:
        if 'i' in request.GET:
            search_types.append("Info Search")
        if 'd' in request.GET:
            search_types.append("Download Search")
    else:
        search_types.append("Info Search")
        search_types.append("Download Search")
    d_results_unformatted = scraper_handler.search(search_txt)
    d_results = list()
    i_results = list()
    for a in d_results_unformatted:
        for b in a:
            d_results.append(b)
    return render(request, "Scraper/search_results.html", {
        "search_text": search_txt,
        "i_results": i_results,
        "d_results": d_results,
        "search_types": search_types,
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
