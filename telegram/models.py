from django.db import models
from django.contrib.auth.models import User

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='telegram_habits')
    place = models.CharField(max_length=255)
    time = models.TimeField()
    action = models.CharField(max_length=255)
    is_pleasant = models.BooleanField(default=False)
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    frequency = models.PositiveIntegerField(default=1)
    reward = models.CharField(max_length=255, null=True, blank=True)
    estimated_time = models.PositiveIntegerField()
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.action
