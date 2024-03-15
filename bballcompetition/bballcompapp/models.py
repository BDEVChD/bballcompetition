from django.db import models

class Team(models.Model):
    team_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

class Game(models.Model):
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_games')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_games')
    start_time = models.DateTimeField()
    start_time_zone = models.CharField(max_length=10)
    end_time = models.DateTimeField(null=True, blank=True)
    end_time_zone = models.CharField(max_length=10, null=True, blank=True)
    current_period = models.IntegerField(null=True, blank=True)
    home_team_score = models.IntegerField(default=0)
    away_team_score = models.IntegerField(default=0)

class GameUpdate(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='updates')
    update_timestamp = models.DateTimeField()
    update_type = models.CharField(max_length=10)


class User(models.Model):
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)