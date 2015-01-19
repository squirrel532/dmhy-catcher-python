from django.conf.urls import url, patterns

urlpatterns = patterns('dmhy.views',
        url(r'^tasklist/', 'tasklist'),
        url(r'^resourcelist/(?P<tid>[0-9]*)', 'resourcelist'),
        url(r'^history/', 'records'),
        url(r'^search/', 'search'),
        )
