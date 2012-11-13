from django.template.response import TemplateResponse

import models

def team_list(request):
    """
    Lists all teams in the Database
    """
    teams = models.Team.objects.all().order_by('name')
    return TemplateResponse(request, 'softball/teams/list.html', {
        'teams': teams,
    })

