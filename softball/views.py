from django.template.response import TemplateResponse

import models

def team_list(request):
    """
    Lists all teams in the Database
    """
    return TemplateResponse(request, 'softball/teams/list.html', {
        'teams': models.Team.objects.all(),
    })

