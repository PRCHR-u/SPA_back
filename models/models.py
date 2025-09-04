from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
import datetime


class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь', related_name='models_habits')
    place = models.CharField(max_length=255, verbose_name='место')
    time = models.TimeField(verbose_name='время')
    action = models.CharField(max_length=255, verbose_name='действие')
    is_pleasant = models.BooleanField(default=False, verbose_name='приятная привычка')
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='связанная привычка')
    frequency = models.PositiveSmallIntegerField(default=1, verbose_name='периодичность в днях')
    reward = models.CharField(max_length=255, null=True, blank=True, verbose_name='награда')
    estimated_time = models.DurationField(verbose_name='время на выполнение')
    is_public = models.BooleanField(default=False, verbose_name='публичная привычка')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='время создания')

    def __str__(self):
        return f'Я буду {self.action} в {self.time} в {self.place}'

    def clean(self):
        if self.reward and self.related_habit:
            raise ValidationError('Нельзя одновременно указывать вознаграждение и связанную привычку.')

        if self.is_pleasant and (self.reward or self.related_habit):
            raise ValidationError('У приятной привычки не может быть вознаграждения или связанной привычки.')

        if self.estimated_time > datetime.timedelta(minutes=2):
            raise ValidationError('Время выполнения должно быть не больше 2 минут.')

        if self.frequency > 7:
            raise ValidationError('Нельзя создавать привычку с периодичностью больше 7 дней.')

        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError('В связанные привычки могут попадать только привычки с признаком приятной привычки.')

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'
