from django.urls import re_path
from django.contrib import admin

from . import views, feeds
from .api import views as api


admin.autodiscover()

app_name = 'name'
urlpatterns = [
    re_path(r'^$', views.landing, name='landing'),
    re_path(r'^about/$', views.about, name='about'),
    re_path(r'^export/$', views.export, name='export'),
    re_path(r'^export.json$', views.export_json, name='export_json'),
    re_path(r'^feed/$', feeds.NameAtomFeed(), name='feed'),
    re_path(r'^label/(?P<name_value>.*)$', views.label, name='label'),
    re_path(r'^locations.json$', api.locations_json, name='locations-json'),
    re_path(r'^map/$', views.locations, name='map'),
    re_path(r'^opensearch.xml$', views.opensearch, name='opensearch'),
    re_path(r'^search/$', views.SearchView.as_view(), name='search'),
    re_path(r'^search.json$', api.search_json, name="search-json"),
    re_path(r'^stats.json$', api.stats_json, name='stats-json'),
    re_path(r'^stats/$', views.stats, name='stats'),
    re_path(r'^(?P<name_id>.*).json$', api.name_json, name='detail-json'),
    re_path(r'^(?P<name_id>.*).mads.xml$', views.mads_serialize, name='mads-serialize'),
    re_path(r'^(?P<name_id>[^/]+)/', views.detail, name='detail')
]
