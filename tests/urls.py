from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin
from name import urls

admin.autodiscover()

urlpatterns = [
    url(r'^name/', include(urls)),
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls))]
