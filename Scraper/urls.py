from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search/$', views.search_page, name='search-page'),
    url(r'^search/(?P<search_txt>[0-9a-zA-Z _!@$|:;&*()"\'.,<>+=`-]+)/$',
        views.search,
        name='search'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^details/(?P<anime_id>[0-9]+)/$',
        views.DetailView.as_view(),
        name='details'),
]
