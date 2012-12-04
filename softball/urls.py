from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template, redirect_to


urlpatterns = patterns('',
    url(r'^$', redirect_to, { 'url': 'team', }, name='softball_home'),
    url(r'^team/$', 'softball.views.team_list', name='team_list'),
    url(r'^team/create/$', 'softball.views.team_edit', name='team_create'),
    url(r'^team/(?P<team_id>\d+)/$', 'softball.views.team_view',
        name='team_view'),
    url(r'^team/(?P<team_id>\d+)/edit/$', 'softball.views.team_edit',
        name='team_edit'),
    url(r'^player/$', 'softball.views.player_list', name='player_list'),
    url(r'^player/create/$', 'softball.views.player_edit',
        name='player_create'),
    url(r'^player/(?P<player_id>\d+)/$', 'softball.views.player_view',
        name='player_view'),
    url(r'^player/(?P<player_id>\d+)/edit/$', 'softball.views.player_edit',
        name='player_edit'),
    url(r'^game/$', 'softball.views.game_list', name='game_list'),
    url(r'^game/create/$', 'softball.views.game_edit', name='game_create'),
    url(r'^game/(?P<game_id>\d+)/$', 'softball.views.game_view',
        name='game_view'),
    url(r'^game/(?P<game_id>\d+)/edit/$', 'softball.views.game_edit',
        name='game_edit'),
)
