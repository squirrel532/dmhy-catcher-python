from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^dmhy/admin/', include(admin.site.urls)),
    url(r'^dmhy/.*$',  'dmhy.views.index' ),
)
