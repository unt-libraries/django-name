from django.conf.urls import patterns, include, url
from django.contrib import admin
from name import urls

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^name/', include(urls)),
    url(r'^admin/', include(admin.site.urls))
)
