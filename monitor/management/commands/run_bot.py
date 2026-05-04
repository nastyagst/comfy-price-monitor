import telebot
from django.core.management.base import BaseCommand
from django.conf import settings
from monitor.services import get_user_alerts_list


class Command(BaseCommand):
    def handle(self, *args, **options):
        bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)

        @bot.message_handler(commands=["list"])
        def list_alerts(message):
            response = get_user_alerts_list()
            bot.reply_to(message, response, parse_mode="HTML")

        print("Бот запущений. Напиши /list у телеграм, щоб отримати список своїх товарів.")
        bot.polling()
