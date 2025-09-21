from celery import shared_task
from django.conf import settings
from telegram import Bot
from .models import Habit
from datetime import datetime


@shared_task
def send_reminders():
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    now = datetime.now().time()
    habits = Habit.objects.filter(time__hour=now.hour, time__minute=now.minute)

    for habit in habits:
        today = datetime.now().date()
        days_since_creation = (today - habit.created_at.date()).days
        if days_since_creation % habit.frequency == 0:
            message = f'Напоминание: {habit}'
            if habit.reward:
                message += f'\nНаграда: {habit.reward}'
            elif habit.related_habit:
                message += (
                    f'\nПриятная привычка: {habit.related_habit}'
                )

            bot.send_message(
                chat_id=settings.TELEGRAM_CHAT_ID,
                text=message
            )
