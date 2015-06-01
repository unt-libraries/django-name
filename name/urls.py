from django.conf.urls import url
from django.contrib import admin

from . import views, feeds
from .api import views as api


admin.autodiscover()

urlpatterns = [
    url(r'^$', views.landing, name='landing'),
    url(r'about/$', views.about, name='about'),
    url(r'export/$', views.export, name='export'),
    url(r'feed/$', feeds.NameAtomFeed(), name='feed'),
    url(r'label/(?P<name_value>.*)$', views.label, name='label'),
    url(r'locations.json/$', api.locations_json, name='locations-json'),
    url(r'map/$', views.locations, name='map'),
    url(r'opensearch.xml$', views.opensearch, name='opensearch'),
    url(r'search/$', views.SearchView.as_view(), name='search'),
    url(r'search.json$', api.search_json, name="search-json"),
    url(r'stats.json/$', api.stats_json, name='stats-json'),
    url(r'stats/$', views.stats, name='stats'),
    url(r'(?P<name_id>.*).json$', api.name_json, name='detail-json'),
    url(r'(?P<name_id>.*).mads.xml$', views.mads_serialize, name='mads-serialize'),
    url(r'(?P<name_id>[^/]+)/', views.detail, name='detail')
]
