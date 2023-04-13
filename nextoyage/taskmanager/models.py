from django.db import models
from datetime import datetime, timedelta


class Tache(models.Model):
    tache_text = models.CharField("Intitulé", max_length=200)
    frequence_int = models.PositiveIntegerField("Fréquence (jours)")
    duration = models.PositiveIntegerField("Durée (min)")

    def __str__(self):
        return self.tache_text

    @property
    def last_session(self):
        sessions = self.sessionmenage_set.all()
        if len(sessions) > 0:
            return sessions.last().quand
        else:
            return None

    @property
    def due(self):
        if self.days_late > 0:
            return True
        else:
            return False

    @property
    def days_late(self):
        last = self.last_session
        if last is None:
            return float('inf')
        today = datetime.now().date()
        return (today-last).days - self.frequence_int


class SessionMenage(models.Model):
    tache = models.ForeignKey(Tache, on_delete=models.CASCADE)
    quand = models.DateField("Quand ?")
    real_duration = models.PositiveIntegerField("Durée réelle (min)")

    class Meta:
        ordering = ('quand', )
    # def __str__(self):
    #     return datetime.strftime("dd/mm/Y", self.quand)
