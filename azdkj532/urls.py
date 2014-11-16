from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^dmhy/admin/', include(admin.site.urls)),
    url(r'^dmhy/history/',  'dmhy.views.history' ),
    url(r'^dmhy/$',  'dmhy.views.index' ),
    url(r'^dmhy/api/tasklist/', 'dmhy.views.tasklist'),
    url(r'^dmhy/api/resourcelist/(?P<tid>[0-9]*)', 'dmhy.views.resourcelist'),
    url(r'^dmhy/api/history/', 'dmhy.views.records'),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
