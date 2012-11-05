from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('softball.views',
    url(r'^$', 'team_list', name='team_list'),
)
