import asyncio
import traceback
from celery import shared_task
from django.conf import settings
from telegram import Bot
from .models import Habit
from datetime import datetime


@shared_task
def send_reminders():
    print("--- Starting send_reminders task ---")
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    now = datetime.now().time()
    # Temporarily remove time filter to process all habits
    # habits = Habit.objects.filter(time__hour=now.hour, time__minute=now.minute)
    habits = Habit.objects.all()
    print(f"Found {habits.count()} habits in total.")

    for habit in habits:
        print(f"\n--- Processing habit: '{habit.action}' ---")
        today = datetime.now().date()
        days_since_creation = (today - habit.created_at.date()).days
        print(f"Days since creation: {days_since_creation}, Frequency: {habit.frequency}")
        if days_since_creation % habit.frequency == 0:
            print("Frequency condition met.")
            message = f'Напоминание: {habit}'
            if habit.reward:
                message += f'\nНаграда: {habit.reward}'
            elif habit.related_habit:
                message += (
                    f'\nПриятная привычка: {habit.related_habit}'
                )

            chat_id = habit.user.telegram_chat_id
            print(f"Target Chat ID: {chat_id}")
            print(f"Message: {message}")

            try:
                print("Attempting to send message via asyncio...")
                asyncio.run(bot.send_message(
                    chat_id=chat_id,
                    text=message
                ))
                print("Message sent successfully!")
            except Exception as e:
                print(f"!!! ERROR SENDING MESSAGE !!!")
                print(f"Error type: {type(e).__name__}")
                print(f"Error details: {e}")
                # print(f"{traceback.format_exc()}")
        else:
            print("Frequency condition NOT met. Skipping.")
    print("\n--- Task finished ---")
