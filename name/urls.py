from django.urls import path, re_path
from django.contrib import admin

from . import views, feeds
from .api import views as api


admin.autodiscover()

app_name = 'name'
urlpatterns = [
    path('', views.landing, name='landing'),
    path('about/', views.about, name='about'),
    path('export/', views.export, name='export'),
    path('export.json', views.export_json, name='export_json'),
    path('feed/', feeds.NameAtomFeed(), name='feed'),
    re_path(r'label/(?P<name_value>.*)$', views.label, name='label'),
    path('locations.json', api.locations_json, name='locations-json'),
    path('map/', views.locations, name='map'),
    path('opensearch.xml', views.opensearch, name='opensearch'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('search.json', api.search_json, name="search-json"),
    path('stats.json', api.stats_json, name='stats-json'),
    path('stats/', views.stats, name='stats'),
    path('<slug:name_id>.json', api.name_json, name='detail-json'),
    path('<slug:name_id>.mads.xml', views.mads_serialize, name='mads-serialize'),
    path('<slug:name_id>/', views.detail, name='detail')
]
