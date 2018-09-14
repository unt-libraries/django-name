from django.conf.urls import include, url
from django.contrib import admin
from name import urls

admin.autodiscover()

urlpatterns = [
    url(r'^name/', include(urls)),
    url(r'^admin/', admin.site.urls)
]
