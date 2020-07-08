from django.db import models
from django.utils import timezone


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return "{user} entered at {entered} {leaved}".format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved= "leaved at " + str(self.leaved_at) if self.leaved_at else "not leaved"
        )

    def get_duration(self):
        time = timezone.localtime() if not self.leaved_at else timezone.localtime(self.leaved_at)
        entered_at = timezone.localtime(self.entered_at)
        duration = time - entered_at
        return duration

    def is_visit_long(self, minutes=60):
        entered_at = timezone.localtime(self.entered_at)
        duration = self.get_duration()
        leaved_at = timezone.localtime(self.leaved_at) if self.leaved_at else False

        if leaved_at:
            timedelta = leaved_at - entered_at
            spent_minutes = timedelta.total_seconds() // 60

            return spent_minutes >= minutes
        else:
            return duration.total_seconds() // 60 >= minutes


def format_duration(duration):
    total_seconds = duration.total_seconds()
    hours = int(total_seconds // 3600)
    total_seconds = total_seconds - hours * 3600
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds - minutes * 60)

    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
