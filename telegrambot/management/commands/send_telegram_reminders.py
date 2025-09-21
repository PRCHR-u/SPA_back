from django.core.management.base import BaseCommand
from telegrambot.tasks import send_reminders
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Send Telegram reminders for habits due now'
    
    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS(
                f'Starting Telegram reminders sending at {datetime.now()}'
            )
        )
        
        try:
            # Вызываем задачу напрямую (синхронно)
            send_reminders()
            self.stdout.write(
                self.style.SUCCESS('Telegram reminders sent successfully!')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error sending reminders: {e}')
            )
            logger.error(f'Error in send_telegram_reminders command: {e}')
