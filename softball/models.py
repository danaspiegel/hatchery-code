from decimal import Decimal

from django.db import models

import calc


class Team(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=150, db_index=True)


    def __unicode__(self):
        return self.name


    def player_count(self):
        return self.players.count()


class Player(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=150, unique=True)
    number = models.PositiveIntegerField()
    team = models.ForeignKey('Team', related_name='players')

    class Meta:
        ordering = ["name", ]

    def __unicode__(self):
        """
        >>> p = Player(name='a b')
        >>> unicode(p)
        'a b ()'
        >>> p = Player(name='a b', number=1)
        >>> unicode(p)
        'a b (1)'
        """
        return u'{0} #{1} - {2}'.format(self.name, self.number or 'N/A',
                                       self.team.name)

    @property
    def hits(self):
        """
        Returns the total hits, doubles, triples, and home_runs

        >>> from datetime import date
        >>> g1, created = Game.objects.get_or_create(game_date=date(2009, 01, 01), score=5, opponent_score=1, opponent="Test Opponent 1")
        >>> g2, created = Game.objects.get_or_create(game_date=date(2009, 02, 01), score=2, opponent_score=3, opponent="Test Opponent 2")
        >>> g3, created = Game.objects.get_or_create(game_date=date(2009, 03, 01), score=2, opponent_score=3, opponent="Test Opponent 3")
        >>> g4, created = Game.objects.get_or_create(game_date=date(2009, 04, 01), score=2, opponent_score=3, opponent="Test Opponent 4")
        >>> g5, created = Game.objects.get_or_create(game_date=date(2009, 05, 01), score=2, opponent_score=3, opponent="Test Opponent 5")
        >>> g6, created = Game.objects.get_or_create(game_date=date(2009, 06, 01), score=2, opponent_score=3, opponent="Test Opponent 6")
        >>> g7, created = Game.objects.get_or_create(game_date=date(2009, 07, 01), score=2, opponent_score=3, opponent="Test Opponent 7")
        >>> g8, created = Game.objects.get_or_create(game_date=date(2009, 01, 01), score=2, opponent_score=3, opponent="Test Opponent 8")
        >>> p, created = Player.objects.get_or_create(first_name="Test", last_name="Player")
        >>> p.hits
        0
        >>> Statistic(player=p, game=g1, singles=1, doubles=0, triples=0, home_runs=0).save()
        >>> Statistic(player=p, game=g2, singles=1, doubles=0, triples=0, home_runs=0).save()
        >>> p.hits
        2

        Test the accumulation of stats
        >>> Statistic(player=p, game=g3, singles=0, doubles=0, triples=0, home_runs=0).save()
        >>> p.hits
        2
        >>> Statistic(player=p, game=g4, singles=1, doubles=0, triples=0, home_runs=0).save()
        >>> p.hits
        3
        >>> Statistic(player=p, game=g5, singles=0, doubles=1, triples=0, home_runs=0).save()
        >>> p.hits
        4
        >>> Statistic(player=p, game=g6, singles=0, doubles=0, triples=1, home_runs=0).save()
        >>> p.hits
        5
        >>> Statistic(player=p, game=g7, singles=0, doubles=0, triples=0, home_runs=1).save()
        >>> p.hits
        6
        >>> Statistic(player=p, game=g8, singles=1, doubles=2, triples=3, home_runs=4).save()
        >>> p.hits
        16

        Clear out the Statistics, and test a single statistic
        >>> p.statistics.all().delete()
        >>> Statistic(player=p, game=g1, singles=0, doubles=0, triples=0, home_runs=0).save()
        >>> p.hits
        0
        >>> p.statistics.all().delete()
        >>> Statistic(player=p, game=g2, singles=1, doubles=0, triples=0, home_runs=0).save()
        >>> p.hits
        1
        >>> p.statistics.all().delete()
        >>> Statistic(player=p, game=g3, singles=0, doubles=1, triples=0, home_runs=0).save()
        >>> p.hits
        1
        >>> p.statistics.all().delete()
        >>> Statistic(player=p, game=g4, singles=0, doubles=0, triples=1, home_runs=0).save()
        >>> p.hits
        1
        >>> p.statistics.all().delete()
        >>> Statistic(player=p, game=g5, singles=0, doubles=0, triples=0, home_runs=1).save()
        >>> p.hits
        1
        >>> p.statistics.all().delete()
        >>> Statistic(player=p, game=g6, singles=1, doubles=2, triples=3, home_runs=4).save()
        >>> p.hits
        10

        Make sure we clean up from these tests
        >>> Statistic.objects.all().delete()
        >>> Game.objects.all().delete()
        >>> Player.objects.all().delete()
        """
        return reduce(lambda total, s: total + s.hits, self.statistics.all(), 0)

    
    @property
    def walks(self):
        """
        Returns the total number of walks for this player

        >>> from datetime import date
        >>> g1, created = Game.objects.get_or_create(game_date=date(2009, 01, 01), score=5, opponent_score=1, opponent="Test Opponent 1")
        >>> g2, created = Game.objects.get_or_create(game_date=date(2009, 02, 01), score=2, opponent_score=3, opponent="Test Opponent 2")
        >>> g3, created = Game.objects.get_or_create(game_date=date(2009, 03, 01), score=2, opponent_score=3, opponent="Test Opponent 3")
        >>> g4, created = Game.objects.get_or_create(game_date=date(2009, 04, 01), score=2, opponent_score=3, opponent="Test Opponent 4")
        >>> p, created = Player.objects.get_or_create(first_name="Test", last_name="Player")
        >>> p.walks
        0
        >>> Statistic(player=p, game=g1, hits=1, doubles=0, triples=0, home_runs=0).save()
        >>> Statistic(player=p, game=g2, hits=1, doubles=0, triples=0, home_runs=0).save()
        >>> p.walks
        0
        >>> Statistic(player=p, game=g3, walks=1, hits=0, doubles=0, triples=0, home_runs=0).save()
        >>> p.walks
        1
        >>> Statistic(player=p, game=g4, walks=2, hits=0, doubles=0, triples=0, home_runs=0).save()
        >>> p.walks
        3

        Make sure we clean up from these tests
        >>> Statistic.objects.all().delete()
        >>> Game.objects.all().delete()
        >>> Player.objects.all().delete()
        """
        return reduce(lambda total, s: total + s.walks, self.statistics.all(), 0)

    
    @property
    def runs(self):
        """
        Returns the total number of walks for this player

        >>> from datetime import date
        >>> g1, created = Game.objects.get_or_create(game_date=date(2009, 01, 01), score=5, opponent_score=1, opponent="Test Opponent 1")
        >>> g2, created = Game.objects.get_or_create(game_date=date(2009, 02, 01), score=2, opponent_score=3, opponent="Test Opponent 2")
        >>> g3, created = Game.objects.get_or_create(game_date=date(2009, 03, 01), score=2, opponent_score=3, opponent="Test Opponent 3")
        >>> g4, created = Game.objects.get_or_create(game_date=date(2009, 04, 01), score=2, opponent_score=3, opponent="Test Opponent 4")
        >>> p, created = Player.objects.get_or_create(first_name="Test", last_name="Player")
        >>> p.runs
        0
        >>> Statistic(player=p, game=g1, runs=1, doubles=0, triples=0, home_runs=0).save()
        >>> Statistic(player=p, game=g2, runs=1, doubles=0, triples=0, home_runs=0).save()
        >>> p.runs
        2
        >>> Statistic(player=p, game=g3, walks=1, runs=0, doubles=0, triples=0, home_runs=0).save()
        >>> p.runs
        2
        >>> Statistic(player=p, game=g4, walks=2, runs=1, doubles=0, triples=0, home_runs=0).save()
        >>> p.runs
        3

        Make sure we clean up from these tests
        >>> Statistic.objects.all().delete()
        >>> Game.objects.all().delete()
        >>> Player.objects.all().delete()
        """
        return reduce(lambda total, s: total + s.runs, self.statistics.all(), 0)


    def singles(self):
        """
        Returns the total number of walks for this player

        >>> from datetime import date
        >>> g1, created = Game.objects.get_or_create(game_date=date(2009, 01, 01), score=5, opponent_score=1, opponent="Test Opponent 1")
        >>> g2, created = Game.objects.get_or_create(game_date=date(2009, 02, 01), score=2, opponent_score=3, opponent="Test Opponent 2")
        >>> g3, created = Game.objects.get_or_create(game_date=date(2009, 03, 01), score=2, opponent_score=3, opponent="Test Opponent 3")
        >>> g4, created = Game.objects.get_or_create(game_date=date(2009, 04, 01), score=2, opponent_score=3, opponent="Test Opponent 4")
        >>> p, created = Player.objects.get_or_create(first_name="Test", last_name="Player")
        >>> p.singles
        0
        >>> Statistic(player=p, game=g1, singles=1, doubles=0, triples=0, home_runs=0).save()
        >>> Statistic(player=p, game=g2, singles=1, doubles=0, triples=0, home_runs=0).save()
        >>> p.singles
        2
        >>> Statistic(player=p, game=g3, walks=1, singles=0, doubles=0, triples=0, home_runs=0).save()
        >>> p.singles
        2
        >>> Statistic(player=p, game=g4, walks=2, singles=1, doubles=0, triples=0, home_runs=0).save()
        >>> p.singles
        3

        Make sure we clean up from these tests
        >>> Statistic.objects.all().delete()
        >>> Game.objects.all().delete()
        >>> Player.objects.all().delete()
        """
        return reduce(lambda total, s: total + s.singles, self.statistics.all(), 0)


    @property
    def at_bats(self):
        """
        Returns the total number of walks for this player

        >>> from datetime import date
        >>> g1, created = Game.objects.get_or_create(game_date=date(2009, 01, 01), score=5, opponent_score=1, opponent="Test Opponent 1")
        >>> g2, created = Game.objects.get_or_create(game_date=date(2009, 02, 01), score=2, opponent_score=3, opponent="Test Opponent 2")
        >>> g3, created = Game.objects.get_or_create(game_date=date(2009, 03, 01), score=2, opponent_score=3, opponent="Test Opponent 3")
        >>> p, created = Player.objects.get_or_create(first_name="Test", last_name="Player")
        >>> p.at_bats
        0
        >>> Statistic(player=p, game=g1, at_bats=1).save()
        >>> Statistic(player=p, game=g2, at_bats=1).save()
        >>> p.at_bats
        2
        >>> Statistic(player=p, game=g3, at_bats=3).save()
        >>> p.at_bats
        5

        Make sure we clean up from these tests
        >>> Statistic.objects.all().delete()
        >>> Game.objects.all().delete()
        >>> Player.objects.all().delete()
        """
        return reduce(lambda total, s: total + s.at_bats, self.statistics.all(), 0)


    @property
    def doubles(self):
        """
        Returns the total number of walks for this player

        >>> from datetime import date
        >>> g1, created = Game.objects.get_or_create(game_date=date(2009, 01, 01), score=5, opponent_score=1, opponent="Test Opponent 1")
        >>> g2, created = Game.objects.get_or_create(game_date=date(2009, 02, 01), score=2, opponent_score=3, opponent="Test Opponent 2")
        >>> g3, created = Game.objects.get_or_create(game_date=date(2009, 03, 01), score=2, opponent_score=3, opponent="Test Opponent 3")
        >>> p, created = Player.objects.get_or_create(first_name="Test", last_name="Player")
        >>> p.doubles
        0
        >>> Statistic(player=p, game=g1, doubles=1).save()
        >>> Statistic(player=p, game=g2, doubles=1).save()
        >>> p.doubles
        2
        >>> Statistic(player=p, game=g3, doubles=3).save()
        >>> p.doubles
        5

        Make sure we clean up from these tests
        >>> Statistic.objects.all().delete()
        >>> Game.objects.all().delete()
        >>> Player.objects.all().delete()
        """
        return reduce(lambda total, s: total + s.doubles, self.statistics.all(), 0)


    @property
    def triples(self):
        """
        Returns the total number of walks for this player

        >>> from datetime import date
        >>> g1, created = Game.objects.get_or_create(game_date=date(2009, 01, 01), score=5, opponent_score=1, opponent="Test Opponent 1")
        >>> g2, created = Game.objects.get_or_create(game_date=date(2009, 02, 01), score=2, opponent_score=3, opponent="Test Opponent 2")
        >>> g3, created = Game.objects.get_or_create(game_date=date(2009, 03, 01), score=2, opponent_score=3, opponent="Test Opponent 3")
        >>> p, created = Player.objects.get_or_create(first_name="Test", last_name="Player")
        >>> p.triples
        0
        >>> Statistic(player=p, game=g1, triples=1).save()
        >>> Statistic(player=p, game=g2, triples=1).save()
        >>> p.triples
        2
        >>> Statistic(player=p, game=g3, triples=3).save()
        >>> p.triples
        5

        Make sure we clean up from these tests
        >>> Statistic.objects.all().delete()
        >>> Game.objects.all().delete()
        >>> Player.objects.all().delete()
        """
        return reduce(lambda total, s: total + s.triples, self.statistics.all(), 0)


    @property
    def home_runs(self):
        """
        Returns the total number of home runs for this player

        >>> from datetime import date
        >>> g1, created = Game.objects.get_or_create(game_date=date(2009, 01, 01), score=5, opponent_score=1, opponent="Test Opponent 1")
        >>> g2, created = Game.objects.get_or_create(game_date=date(2009, 02, 01), score=2, opponent_score=3, opponent="Test Opponent 2")
        >>> g3, created = Game.objects.get_or_create(game_date=date(2009, 03, 01), score=2, opponent_score=3, opponent="Test Opponent 3")
        >>> p, created = Player.objects.get_or_create(first_name="Test", last_name="Player")
        >>> p.home_runs
        0
        >>> Statistic(player=p, game=g1, home_runs=1).save()
        >>> Statistic(player=p, game=g2, home_runs=1).save()
        >>> p.home_runs
        2
        >>> Statistic(player=p, game=g3, home_runs=3).save()
        >>> p.home_runs
        5

        Make sure we clean up from these tests
        >>> Statistic.objects.all().delete()
        >>> Game.objects.all().delete()
        >>> Player.objects.all().delete()
        """
        return reduce(lambda total, s: total + s.home_runs, self.statistics.all(), 0)


    @property
    def rbis(self):
        """
        Returns the total number of rbis for this player

        >>> from datetime import date
        >>> g1, created = Game.objects.get_or_create(game_date=date(2009, 01, 01), score=5, opponent_score=1, opponent="Test Opponent 1")
        >>> g2, created = Game.objects.get_or_create(game_date=date(2009, 02, 01), score=2, opponent_score=3, opponent="Test Opponent 2")
        >>> g3, created = Game.objects.get_or_create(game_date=date(2009, 03, 01), score=2, opponent_score=3, opponent="Test Opponent 3")
        >>> g4, created = Game.objects.get_or_create(game_date=date(2009, 04, 01), score=2, opponent_score=3, opponent="Test Opponent 4")
        >>> p, created = Player.objects.get_or_create(first_name="Test", last_name="Player")
        >>> p.rbis
        0
        >>> Statistic(player=p, game=g1, rbis=1).save()
        >>> Statistic(player=p, game=g2, rbis=1).save()
        >>> p.rbis
        2
        >>> Statistic(player=p, game=g3, rbis=0).save()
        >>> p.rbis
        2
        >>> Statistic(player=p, game=g4, rbis=1).save()
        >>> p.rbis
        3

        Make sure we clean up from these tests
        >>> Statistic.objects.all().delete()
        >>> Game.objects.all().delete()
        >>> Player.objects.all().delete()
        """
        return reduce(lambda total, s: total + s.rbis, self.statistics.all(), 0)


    @property
    def batting_average(self):
        """
        >>> from datetime import date
        >>> g1, created = Game.objects.get_or_create(game_date=date(2009, 01, 01), score=5, opponent_score=1, opponent="Test Opponent 1")
        >>> g2, created = Game.objects.get_or_create(game_date=date(2009, 02, 01), score=2, opponent_score=3, opponent="Test Opponent 2")
        >>> g3, created = Game.objects.get_or_create(game_date=date(2009, 03, 01), score=2, opponent_score=3, opponent="Test Opponent 3")
        >>> g4, created = Game.objects.get_or_create(game_date=date(2009, 04, 01), score=2, opponent_score=3, opponent="Test Opponent 4")
        >>> g5, created = Game.objects.get_or_create(game_date=date(2009, 05, 01), score=2, opponent_score=3, opponent="Test Opponent 5")
        >>> p, created = Player.objects.get_or_create(first_name="Test", last_name="Player")
        >>> p.average
        Decimal("0")

        >>> Statistic(player=p, game=g1, at_bats=4, walks=2, singles=1).save()
        >>> p.average
        Decimal("0.25")
        >>> Statistic(player=p, game=g2, at_bats=0, walks=0, doubles=0).save()
        >>> p.average
        Decimal("0.25")
        >>> Statistic(player=p, game=g3, at_bats=4, walks=1, triples=2, home_runs=1).save()
        >>> p.average
        Decimal("0.5")
        >>> Statistic(player=p, game=g4, at_bats=2, walks=1, home_runs=0).save()
        >>> p.average
        Decimal("0.4")
        >>> Statistic(player=p, game=g5, at_bats=1, walks=0, home_runs=1).save()
        >>> p.average
        Decimal("0.4545454545454545454545454545")

        Make sure we clean up from these tests
        >>> Statistic.objects.all().delete()
        >>> Game.objects.all().delete()
        >>> Player.objects.all().delete()
        """
        if not self.statistics.count():
            return Decimal("0")
        if self.hits > self.at_bats:
            raise ValueError("hits must be <= at_bats")
        return calc.average(self.at_bats, self.hits)


    @property
    def on_base_percentage(self):
        """
        >>> from datetime import date
        >>> g1, created = Game.objects.get_or_create(game_date=date(2009, 01, 01), score=5, opponent_score=1, opponent="Test Opponent 1")
        >>> g2, created = Game.objects.get_or_create(game_date=date(2009, 02, 01), score=2, opponent_score=3, opponent="Test Opponent 2")
        >>> g3, created = Game.objects.get_or_create(game_date=date(2009, 03, 01), score=2, opponent_score=3, opponent="Test Opponent 3")
        >>> p, created = Player.objects.get_or_create(first_name="Test", last_name="Player")
        >>> p.on_base_percentage
        Decimal("0")
        >>> Statistic(player=p, game=g1, at_bats=0, walks=0, singles=0).save()
        >>> p.on_base_percentage
        Decimal("0")
        >>> Statistic(player=p, game=g2, at_bats=3, walks=1, doubles=2).save()
        >>> p.on_base_percentage
        Decimal("0.75")
        >>> Statistic(player=p, game=g3, at_bats=3, walks=1, home_runs=0).save()
        >>> p.on_base_percentage
        Decimal("0.5")

        Make sure we clean up from these tests
        >>> Statistic.objects.all().delete()
        >>> Game.objects.all().delete()
        >>> Player.objects.all().delete()
        """
        if self.hits > self.at_bats:
            raise ValueError("hits must be <= at_bats")
        return calc.on_base_percentage(self.at_bats, self.walks, self.hits)

    
    @property
    def slugging_percentage(self):
        """
        >>> from datetime import date
        >>> g1, created = Game.objects.get_or_create(game_date=date(2009, 01, 01), score=5, opponent_score=1, opponent="Test Opponent 1")
        >>> g2, created = Game.objects.get_or_create(game_date=date(2009, 02, 01), score=2, opponent_score=3, opponent="Test Opponent 2")
        >>> g3, created = Game.objects.get_or_create(game_date=date(2009, 03, 01), score=2, opponent_score=3, opponent="Test Opponent 3")
        >>> g4, created = Game.objects.get_or_create(game_date=date(2009, 04, 01), score=2, opponent_score=3, opponent="Test Opponent 4")
        >>> g5, created = Game.objects.get_or_create(game_date=date(2009, 05, 01), score=5, opponent_score=1, opponent="Test Opponent 5")
        >>> g6, created = Game.objects.get_or_create(game_date=date(2009, 06, 01), score=2, opponent_score=3, opponent="Test Opponent 6")
        >>> g7, created = Game.objects.get_or_create(game_date=date(2009, 07, 01), score=2, opponent_score=3, opponent="Test Opponent 7")
        >>> g8, created = Game.objects.get_or_create(game_date=date(2009, 01, 01), score=2, opponent_score=3, opponent="Test Opponent 8")
        >>> p, created = Player.objects.get_or_create(first_name="Test", last_name="Player")
        >>> p.slugging_percentage
        Decimal("0")

        >>> Statistic(player=p, game=g1, at_bats=3, walks=3, singles=0, doubles=0, triples=0, home_runs=0).save()
        >>> p.slugging_percentage
        Decimal("0")

        >>> Statistic(player=p, game=g2, at_bats=3, walks=0, singles=1, doubles=1, triples=1, home_runs=0).save()
        >>> p.slugging_percentage
        Decimal("1")

        >>> Statistic(player=p, game=g3, at_bats=4, walks=0, singles=1, doubles=1, triples=1, home_runs=1).save()
        >>> p.slugging_percentage
        Decimal("1.6")

        >>> Statistic(player=p, game=g4, at_bats=1, walks=0, singles=1, doubles=0, triples=0, home_runs=0).save()
        >>> p.slugging_percentage
        Decimal("1.545454545454545454545454545")

        >>> Statistic(player=p, game=g5, at_bats=1, walks=0, singles=0, doubles=1, triples=0, home_runs=0).save()
        >>> p.slugging_percentage
        Decimal("1.583333333333333333333333333")

        >>> Statistic(player=p, game=g6, at_bats=1, walks=0, singles=0, doubles=0, triples=1, home_runs=0).save()
        >>> p.slugging_percentage
        Decimal("1.692307692307692307692307692")

        >>> Statistic(player=p, game=g7, at_bats=1, walks=0, singles=0, doubles=0, triples=0, home_runs=1).save()
        >>> p.slugging_percentage
        Decimal("1.857142857142857142857142857")

        >>> Statistic(player=p, game=g8, at_bats=8, walks=0, singles=2, doubles=2, triples=2, home_runs=2).save()
        >>> p.slugging_percentage
        Decimal("2.090909090909090909090909091")

        Make sure we clean up from these tests
        >>> Statistic.objects.all().delete()
        >>> Game.objects.all().delete()
        >>> Player.objects.all().delete()
        """
        if self.hits > self.at_bats:
            raise ValueError("hits must be <= at_bats")
        return calc.slugging_percentage(self.at_bats, self.singles, self.doubles, self.triples, self.home_runs)


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
        if self.away_score > self.home_score:
            return self.away_roster.team
        else:
            return self.home_roster.team


    @property
    def final_score(self):
        """
        Returns the final score of the game, as recorded in the rosters, as a
        tuple (away_score, home_score)
        """
        return self.away_score, self.home_score


    @property
    def home_score(self):
        """
        Returns the score of the home team, as recorded in the home roster
        """


    @property
    def away_score(self):
        """
        Returns the score of the home team, as recorded in the home roster
        """


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
        return self.singles + self.doubles + self.triples + self.home_runs


    @property
    def batting_average(self):
        if self.hits > self.at_bats:
            raise ValueError("hits must be <= at_bats")
        return calc.average(self.at_bats, self.hits)
