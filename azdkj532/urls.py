from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^history/',  'dmhy.views.history' ),
    url(r'^$',  'dmhy.views.index' ),
    url(r'^api/tasklist/', 'dmhy.views.tasklist'),
    url(r'^api/resourcelist/(?P<tid>[0-9]*)', 'dmhy.views.resourcelist'),
    url(r'^api/history/', 'dmhy.views.records'),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
