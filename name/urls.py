from django.conf.urls import patterns, url
from django.contrib import admin
from name import views, feeds


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'stats.json/$', 'name.api.views.stats_json', name='stats-json'),
    url(r'stats/$', 'name.views.stats', name='stats'),
    url(r'label/(?P<name_value>.*)$', 'name.views.label', name='label'),
    url(r'feed/$', feeds.NameAtomFeed(), name='feed'),
    url(r'map/$', 'name.views.map', name='map'),
    url(r'locations.json/$', 'name.api.views.locations_json', name='locations-json'),
    url(r'^$', 'name.views.landing', name='landing'),
    url(r'export/$', 'name.views.export', name='export'),
    url(r'search/$', views.SearchView.as_view(), name='search'),
    url(r'search.json$', 'name.api.views.search_json', name="search-json"),
    url(r'about/$', 'name.views.about', name='about'),
    url(r'(?P<name_id>.*).json$', 'name.api.views.name_json', name='detail-json'),
    url(r'opensearch.xml$', 'name.views.opensearch', name='opensearch'),
    url(
        r'(?P<name_id>.*).mads.xml$',
        'name.views.mads_serialize',
        name='mads-serialize'
    ),
    url(
        r'(?P<name_id>[^/]+)/',
        'name.views.detail',
        name='detail'
    ),
)
