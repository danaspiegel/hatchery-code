from django.contrib import admin

from models import Team, Player, Game, Roster, Statistic


class StatisticAdmin(admin.TabularInline):
    model = Statistic
    fields = ('player', 'at_bats', 'runs', 'singles', 'doubles', 'triples',
              'home_runs', 'rbis', 'walks', )
    max_num = 12
    extra = 12


class TeamAdmin(admin.ModelAdmin):
    search_fields = ('name', 'players__name', )


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'team', )
    search_fields = ('name', 'number', 'team__name', )
    list_filter = ('team', )


class GameAdmin(admin.ModelAdmin):
    pass


class RosterAdmin(admin.ModelAdmin):
    list_display = ('team', 'home_game', 'away_game', )
    inlines = (StatisticAdmin, )


admin.site.register(Team, TeamAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Roster, RosterAdmin)
