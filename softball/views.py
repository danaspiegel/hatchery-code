from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.shortcuts import redirect
from django.template.response import TemplateResponse

import models, forms

def team_list(request):
    paginator = Paginator(models.Team.objects.all().order_by('name'),
                          10)
    page = request.GET.get('page')
    try:
        teams = paginator.page(page)
    except PageNotAnInteger:
        teams = paginator.page(1)
    except EmptyPage:
        teams = paginator.page(paginator.num_pages)
    return TemplateResponse(request, 'softball/team/list.html', {
        'teams': teams,
    })


def team_view(request, team_id):
    try:
        team = models.Team.objects.get(pk=team_id)
    except models.Team.DoesNotExist:
        raise Http404
    return TemplateResponse(request, 'softball/team/view.html', {
        'team': team,
        'record': team.record(),
    })


def team_create(request):
    if request.method == 'POST':
        team_form = forms.TeamForm(request.POST)
        if team_form.is_valid():
            team = team_form.save()
            return redirect('team_view', team_id=team.id)
    else:
        team_form = forms.TeamForm()

    return TemplateResponse(request, 'softball/team/create.html', {
        'team_form': team_form,
    })


def team_edit(request, team_id=None):
    try:
        team = models.Team.objects.get(pk=team_id)
    except models.Team.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        team_form = forms.TeamForm(request.POST, instance=team)
        if team_form.is_valid():
            team = team_form.save()
            return redirect('team_view', team_id=team.id)
    else:
        team_form = forms.TeamForm(instance=team)

    return TemplateResponse(request, 'softball/team/edit.html', {
        'team': team,
        'record': team.record(),
        'team_form': team_form,
    })


def player_list(request):
    paginator = Paginator(models.Player.objects.all().order_by('name'),
                          10)
    page = request.GET.get('page')
    try:
        players = paginator.page(page)
    except PageNotAnInteger:
        players = paginator.page(1)
    except EmptyPage:
        players = paginator.page(paginator.num_pages)
    return TemplateResponse(request, 'softball/player/list.html', {
        'players': players,
    })


def player_view(request, player_id):
    try:
        player = models.Player.objects.get(pk=player_id)
    except models.Team.DoesNotExist:
        raise Http404
    return TemplateResponse(request, 'softball/player/view.html', {
        'player': player,
    })


def player_create(request):
    # if there's a team_id specified, use that team as the preset team for
    # this player
    team = models.Team()
    if request.GET.has_key('team_id'):
        try:
            team = models.Team.objects.get(pk=request.GET['team_id'])
        except models.Team.DoesNotExist, e:
            # Team doesn't exist, so just use an empty team
            pass
    player = models.Player(team=team)

    if request.method == 'POST':
        player_form = forms.PlayerForm(request.POST, instance=player)
        if player_form.is_valid():
            player = player_form.save()
            return redirect('player_view', player_id=player.id)
    else:
        player_form = forms.PlayerForm(instance=player)

    return TemplateResponse(request, 'softball/player/create.html', {
        'player': player,
        'player_form': player_form,
    })


def player_edit(request, player_id):
    try:
        player = models.Player.objects.get(pk=player_id)
    except models.Player.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        player_form = forms.PlayerForm(request.POST, instance=player)
        if player_form.is_valid():
            player = player_form.save()
            return redirect('player_view', player_id=player.id)
    else:
        player_form = forms.PlayerForm(instance=player)

    return TemplateResponse(request, 'softball/player/edit.html', {
        'player': player,
        'player_form': player_form,
    })


def game_list(request):
    paginator = Paginator(models.Game.objects.all().order_by('played_on'),
                          10)
    page = request.GET.get('page')
    try:
        games = paginator.page(page)
    except PageNotAnInteger:
        games = paginator.page(1)
    except EmptyPage:
        games = paginator.page(paginator.num_pages)
    return TemplateResponse(request, 'softball/game/list.html', {
        'games': games,
    })


def game_view(request, game_id):
    try:
        game = models.Game.objects.get(pk=game_id)
    except models.Game.DoesNotExist:
        raise Http404
    return TemplateResponse(request, 'softball/game/view.html', {
        'game': game,
        'away_roster': game.away_roster,
        'home_roster': game.home_roster,
    })


def game_create(request):
    if request.method == 'POST':
        game_form = forms.GameForm(request.POST)
        if game_form.is_valid():
            game = game_form.save()
            return redirect('game_view', game_id=game.id)
    else:
        game_form = forms.GameForm()

    return TemplateResponse(request, 'softball/game/create.html', {
        'game_form': game_form,
    })


def game_edit(request, game_id):
    try:
        game = models.Game.objects.get(pk=game_id)
    except models.Player.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        game_form = forms.GameForm(request.POST, instance=game)
        if game_form.is_valid():
            game = game_form.save()
            return redirect('game_view', game_id=game.id)
    else:
        game_form = forms.GameForm(instance=game)

    return TemplateResponse(request, 'softball/game/edit.html', {
        'game': game,
        'game_form': game_form,
    })


