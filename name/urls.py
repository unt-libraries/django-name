from django.conf.urls import patterns, url
from django.contrib import admin
from name import views, feeds


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'stats.json/$', 'name.api.views.stats_json', name='name_stats_json'),
    url(r'stats/$', 'name.views.stats', name='name_stats'),
    url(r'label/(?P<name_value>.*)$', 'name.views.label', name='name_label'),
    url(r'feed/$', feeds.NameAtomFeed(), name='name_feed'),
    url(r'label/(?P<name_value>.*)$', 'name.views.label', name='name_label'),
    url(r'map/$', 'name.views.map', name='name_map'),
    url(r'map.json/$', 'name.api.views.map_json', name='name_map_json'),
    url(r'^$', 'name.views.landing', name='name_landing'),
    url(r'export/$', 'name.views.export', name='name_export'),
    url(r'search/$', views.SearchView.as_view(), name='name_search'),
    url(r'search.json$', 'name.api.views.get_names', name="name_names"),
    url(r'about/$', 'name.views.about', name='name_about'),
    url(r'(?P<name_id>.*).json$', 'name.api.views.name_json', name='name_json'),
    url(r'opensearch.xml$', 'name.views.opensearch', name='name_opensearch'),
    url(
        r'(?P<name_id>.*).mads.xml$',
        'name.views.mads_serialize',
        name='name_mads_serialize'
    ),
    url(
        r'(?P<name_id>[^/]+)/',
        'name.views.entry_detail',
        name='name_entry_detail'
    ),
)
