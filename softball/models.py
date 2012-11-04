from django.db import models

import calc


class Team(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=150, db_index=True)


    def __unicode__(self):
        return self.name


    def player_count(self):
        pass


class Player(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=150, unique=True)
    number = models.PositiveIntegerField()
    team = models.ForeignKey('Team', related_name='players')

    class Meta:
        ordering = ["name", ]

    def __unicode__(self):
        return u'{0} #{1} - {2}'.format(self.name,
                                        self.number or 'N/A',
                                        self.team.name)

    @property
    def hits(self):
        """
        Returns the total hits, doubles, triples, and home_runs
        """
        pass


    @property
    def walks(self):
        """
        Returns the total number of walks for this player
        """
        pass


    @property
    def runs(self):
        """
        Returns the total number of walks for this player
        """
        pass


    def singles(self):
        """
        Returns the total number of walks for this player
        """
        pass


    @property
    def at_bats(self):
        """
        Returns the total number of walks for this player
        """
        pass


    @property
    def doubles(self):
        """
        Returns the total number of walks for this player
        """
        pass


    @property
    def triples(self):
        """
        Returns the total number of walks for this player
        """
        pass


    @property
    def home_runs(self):
        """
        Returns the total number of home runs for this player
        """
        pass


    @property
    def rbis(self):
        """
        Returns the total number of rbis for this player
        """
        pass


    @property
    def batting_average(self):
        pass


    @property
    def on_base_percentage(self):
        pass

    @property
    def slugging_percentage(self):
        pass


class Game(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    played_on = models.DateTimeField()
    location = models.CharField(max_length=150)
    home_roster = models.OneToOneField('Roster', related_name='home_game')
    away_roster = models.OneToOneField('Roster', related_name='away_game')


    def __unicode__(self):
        return u'{0} - {1}'.format(self.location, self.played_on)


    @property
    def winner(self):
        pass


    @property
    def final_score(self):
        """
        Returns the final score of the game, as recorded in the rosters, as a
        tuple (away_score, home_score)
        """
        pass


    @property
    def home_score(self):
        """
        Returns the score of the home team, as recorded in the home roster
        """
        pass


    @property
    def away_score(self):
        """
        Returns the score of the home team, as recorded in the home roster
        """
        pass


class Roster(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    team = models.ForeignKey('Team', related_name='rosters')


    def __unicode__(self):
        return '{0} - {1}'.format(self.team.name, self.id)


class Statistic(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    player = models.OneToOneField('Player', related_name='statistics')
    at_bats = models.PositiveIntegerField(default=0)
    runs = models.PositiveIntegerField(default=0)
    singles = models.PositiveIntegerField(default=0)
    doubles = models.PositiveIntegerField(default=0)
    triples = models.PositiveIntegerField(default=0)
    home_runs = models.PositiveIntegerField(default=0)
    rbis = models.PositiveIntegerField(default=0)
    walks = models.PositiveIntegerField(default=0)
    roster = models.ForeignKey('Roster', related_name='player_statistics')


    def __unicode__(self):
        return u'{0} - {1}'.format(self.player.name, self.roster)


    @property
    def hits(self):
        pass


    @property
    def batting_average(self):
        pass
