from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100)
    captian = models.CharField(max_length=100)
    mem1 = models.CharField(max_length=100)
    mem2 = models.CharField(max_length=100)
    mem3 = models.CharField(max_length=100)
    mem4 = models.CharField(max_length=100)
    mem5 = models.CharField(max_length=100)
    mem6 = models.CharField(max_length=100)

    def members_list(self):
        return [self.captian, self.mem1, self.mem2, self.mem3, self.mem4, self.mem5, self.mem6]

class Score(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    W = models.IntegerField(default=0)
    L = models.IntegerField(default=0)
    pts = models.IntegerField(default=0)
    matches = models.IntegerField(default=0)

class Match(models.Model):
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='matches_as_team1')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='matches_as_team2')
    scheduled_date = models.DateTimeField()
    team1_sets = models.IntegerField(null=True, blank=True)
    team2_sets = models.IntegerField(null=True, blank=True)
    mvp_name = models.CharField(max_length=100, blank=True, default="")
    is_played = models.BooleanField(default=False)
    played_at = models.DateTimeField(null=True, blank=True)

    def winner(self):
        if not self.is_played:
            return None
        return self.team1 if self.team1_sets > self.team2_sets else self.team2