from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Bot
from telegrambot.models import Habit
from datetime import datetime, time
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Send Telegram reminders for all due habits right now'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--force-time',
            type=str,
            help='Force specific time (format: HH:MM)',
        )
    
    def handle(self, *args, **options):
        force_time = options.get('force_time')
        
        if force_time:
            # Парсим принудительное время
            hour, minute = map(int, force_time.split(':'))
            current_time = time(hour, minute)
            self.stdout.write(
                self.style.WARNING(
                    f'Using forced time: {current_time}'
                )
            )
        else:
            current_time = datetime.now().time()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Sending reminders for time: {current_time}'
            )
        )
        
        try:
            bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
            
            # Получаем привычки для текущего (или принудительного) времени
            habits = Habit.objects.filter(
                time__hour=current_time.hour, 
                time__minute=current_time.minute
            )
            
            for habit in habits:
                if not habit.user or not habit.user.telegram_chat_id:
                    continue
                
                message = f'⏰ Напоминание о привычке:\n'
                message += f'📍 Место: {habit.place}\n'
                message += f'⏰ Время: {habit.time.strftime("%H:%M")}\n'
                message += f'🎯 Действие: {habit.action}\n'
                message += f'⏱ Время на выполнение: {habit.estimated_time} сек.\n'
                
                if habit.reward:
                    message += f'🎁 Награда: {habit.reward}\n'
                elif habit.related_habit:
                    message += f'✨ Связанная привычка: {habit.related_habit.action}\n'
                
                # Отправляем сообщение
                bot.send_message(
                    chat_id=habit.user.telegram_chat_id,
                    text=message
                )
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Sent to user {habit.user.username}: {habit.action}'
                    )
                )
            
            self.stdout.write(
                self.style.SUCCESS('All reminders sent successfully!')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error sending reminders: {e}')
            )
            logger.error(f'Error in send_reminders_now command: {e}')
