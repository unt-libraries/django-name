from django.urls import include, path
from django.conf import settings
from django.contrib import admin
from name import urls

admin.autodiscover()

urlpatterns = [
    path('name/', include(urls)),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
