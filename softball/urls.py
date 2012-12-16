from django.conf.urls import patterns, url
from django.views.generic.simple import redirect_to


urlpatterns = patterns('',
    url(r'^$', redirect_to, { 'url': 'team', }, name='softball_home'),
    url(r'^team/$', 'softball.views.team_list', name='team_list'),
    url(r'^team/create/$', 'softball.views.team_create', name='team_create'),
    url(r'^team/(?P<team_id>\d+)/$', 'softball.views.team_view',
        name='team_view'),
    url(r'^team/(?P<team_id>\d+)/edit/$', 'softball.views.team_edit',
        name='team_edit'),
    url(r'^team/(?P<team_id>\d+)/delete/$', 'softball.views.team_delete',
        name='team_delete'),
    url(r'^player/$', 'softball.views.player_list', name='player_list'),
    url(r'^player/create/$', 'softball.views.player_create',
        name='player_create'),
    url(r'^player/(?P<player_id>\d+)/$', 'softball.views.player_view',
        name='player_view'),
    url(r'^player/(?P<player_id>\d+)/edit/$', 'softball.views.player_edit',
        name='player_edit'),
    url(r'^player/(?P<player_id>\d+)/delete/$', 'softball.views.player_delete',
        name='player_delete'),
    url(r'^game/$', 'softball.views.game_list', name='game_list'),
    url(r'^game/create/$', 'softball.views.game_create', name='game_create'),
    url(r'^game/(?P<game_id>\d+)/$', 'softball.views.game_view',
        name='game_view'),
    url(r'^game/(?P<game_id>\d+)/edit/$', 'softball.views.game_edit',
        name='game_edit'),
    url(r'^game/(?P<game_id>\d+)/delete/$', 'softball.views.game_delete',
        name='game_delete'),
    url(r'^user/$', 'softball.views.user_edit', name='user_edit'),
)
