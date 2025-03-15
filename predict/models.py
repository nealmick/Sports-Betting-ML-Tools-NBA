from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class Game(models.Model):
    CHOICES = (
        ('ATL', 'Atlanta Hawks'),
        ('BKN', 'Brooklyn Nets'),
        ('BOS', 'Boston Celtics'),
        ('CHA', 'Charlotte Hornets'),
        ('CHI', 'Chicago Bulls'),
        ('CLE', 'Cleveland Cavaliers'),
        ('DAL', 'Dallas Mavericks'),
        ('DEN', 'Denver Nuggets'),
        ('DET', 'Detroit Pistons'),
        ('GSW', 'Golden State Warriors'),
        ('HOU', 'Houston Rockets'),
        ('IND', 'Indiana Pacers'),
        ('LAC', 'Los Angeles Clippers'),
        ('LAL', 'Los Angeles Lakers'),
        ('MEM', 'Memphis Grizzlies'),
        ('MIA', 'Miami Heat'),
        ('MIL', 'Milwaukee Bucks'),
        ('MIN', 'Minnesota Timberwolves'),
        ('NOP', 'New Orleans Pelicans'),
        ('NYK', 'New York Knicks'),
        ('OKC', 'Oklahoma City Thunder'),
        ('ORL', 'Orlando Magic'),
        ('PHI', 'Philadelphia 76ers'),
        ('PHX', 'Phoenix Suns'),
        ('POR', 'Portland Trail Blazers'),
        ('SAC', 'Sacramento Kings'),
        ('SAS', 'San Antonio Spurs'),
        ('TOR', 'Toronto Raptors'),
        ('UTA', 'Utah Jazz'),
        ('WAS', 'Washington Wizards'),
        )
    home = models.CharField(max_length=3, choices=CHOICES)
    homecolor = models.CharField(max_length=10)
    visitor = models.CharField(max_length=3, choices=CHOICES)
    visitorcolor = models.CharField(max_length=10)

    gamedate = models.CharField(max_length=10, default=timezone.now().strftime('%Y-%m-%d'))

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    date_posted = models.DateTimeField(default=timezone.now)

    prediction = models.DecimalField(null=True, blank=True, max_digits=4, decimal_places=3)

    gameid = models.CharField(null=True, blank=True, max_length=10)

    home_score = models.CharField(default='0',null=True, blank=True, max_length=3)
    visitor_score = models.CharField(default='0',null=True, blank=True, max_length=3)

    finished = models.BooleanField(default=False)

    home_spread = models.CharField(null=True, blank=True, max_length=10)
    visitor_spread = models.CharField(null=True, blank=True, max_length=10)
    dk_home_spread = models.CharField(null=True, blank=True, max_length=10)
    dk_visitor_spread = models.CharField(null=True, blank=True, max_length=10)

    winner = models.IntegerField(null=True, blank=True, default=0)

    csvid = models.CharField(null=True, blank=True, max_length=10)

    home_score_prediction = models.CharField(null=True, blank=True, max_length=10)
    visitor_score_prediction = models.CharField(null=True, blank=True, max_length=10)

    pmscore = models.FloatField(null=True, blank=True, default=0)

    home_games_won = models.CharField(null=True, blank=True, max_length=10)
    home_games_loss = models.CharField(null=True, blank=True, max_length=10)
    visitor_games_won = models.CharField(null=True, blank=True, max_length=10)
    visitor_games_loss = models.CharField(null=True, blank=True, max_length=10)

    visitor_streak = models.CharField(null=True, blank=True, max_length=10)
    home_streak = models.CharField(null=True, blank=True, max_length=10)

    ev_won = models.CharField(null=True, blank=True, max_length=10)
    ev_margin1 = models.CharField(null=True, blank=True, max_length=10)
    ev_margin2 = models.CharField(null=True, blank=True, max_length=10)
    ev_margin3 = models.CharField(null=True, blank=True, max_length=10)

    margin = models.CharField(null=True, blank=True, max_length=10)
    homeInjury = models.CharField(null=True, blank=True, max_length=1000)
    homeInjuryComplex = models.CharField(null=True, blank=True, max_length=10000)
    visitorInjury = models.CharField(null=True, blank=True, max_length=1000)
    visitorInjuryComplex = models.CharField(null=True, blank=True, max_length=10000)
    removed_players = models.CharField(null=True, blank=True, max_length=1000)
    spread_prediction = models.CharField(null=True, blank=True, max_length=10)

    bet = models.BooleanField(default=False)
    model = models.CharField(default='0', max_length=10)
    complexSpread = models.CharField(null=True, blank=True, max_length=10000)

    home_last_game = models.CharField(null=True, blank=True, max_length=15)
    home_history = models.CharField(null=True, blank=True, max_length=100000)
    home_history2 = models.CharField(null=True, blank=True, max_length=100000)

    visitor_last_game = models.CharField(null=True, blank=True, max_length=15)
    visitor_history = models.CharField(null=True, blank=True, max_length=100000)
    visitor_history2 = models.CharField(null=True, blank=True, max_length=100000)

    p0 = models.CharField(null=True, blank=True, max_length=10)
    p1 = models.CharField(null=True, blank=True, max_length=10)
    p2 = models.CharField(null=True, blank=True, max_length=10)
    p3 = models.CharField(null=True, blank=True, max_length=10)
    p4 = models.CharField(null=True, blank=True, max_length=10)
    p5 = models.CharField(null=True, blank=True, max_length=10)
    p6 = models.CharField(null=True, blank=True, max_length=10)
    p7 = models.CharField(null=True, blank=True, max_length=10)
    p8 = models.CharField(null=True, blank=True, max_length=10)
    p9 = models.CharField(null=True, blank=True, max_length=10)
    p10 = models.CharField(null=True, blank=True, max_length=10)
    p11 = models.CharField(null=True, blank=True, max_length=10)
    p12 = models.CharField(null=True, blank=True, max_length=10)
    p13 = models.CharField(null=True, blank=True, max_length=10)
    p14 = models.CharField(null=True, blank=True, max_length=10)
    p15 = models.CharField(null=True, blank=True, max_length=10)
    p16 = models.CharField(null=True, blank=True, max_length=10)
    p17 = models.CharField(null=True, blank=True, max_length=10)
    p18 = models.CharField(null=True, blank=True, max_length=10)
    simpleRecord = models.BooleanField(default=False)

    def __str__(self):
        return str(self.author)

    def get_absolute_url(self):
        return reverse('edit-predict', kwargs={'pk': self.pk})


class TensorflowModel(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    ip = models.CharField(null=True, blank=True, max_length=50)
    model_number = models.CharField(null=True, blank=True, max_length=50)

    def __str__(self):
        return f"TensorflowModel {self.model_number} by {self.author}"


class PermaGame(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    ip = models.CharField(null=True, blank=True, max_length=50)

    def __str__(self):
        return f"PermaGame by {self.author}"


class Retrain(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    ip = models.CharField(null=True, blank=True, max_length=50)
    model = models.CharField(null=True, blank=True, max_length=50)
    strength = models.CharField(null=True, blank=True, max_length=50)

    def __str__(self):
        return f"Retrain game={self.game_id} model={self.model} by {self.author}"


class ModelReset(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    ip = models.CharField(null=True, blank=True, max_length=50)
    model = models.CharField(null=True, blank=True, max_length=50)

    def __str__(self):
        return f"ModelReset model={self.model} by {self.author}"


class ArbLoad(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    ip = models.CharField(null=True, blank=True, max_length=50)

    def __str__(self):
        return f"ArbLoad by {self.author}"
