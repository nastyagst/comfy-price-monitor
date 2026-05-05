import telebot
from django.core.management.base import BaseCommand
from django.conf import settings
from monitor.services import get_user_alerts_list


class Command(BaseCommand):
    help = "Starts the telegram bot"

    def handle(self, *args, **options):
        bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)

        @bot.message_handler(commands=["start"])
        def start_handler(message):
            bot.reply_to(
                message,
                "Привіт! Я твій монітор цін. Напиши /list, щоб перевірити товари.",
            )

        @bot.message_handler(commands=["list"])
        def list_alerts(message):
            response = get_user_alerts_list()
            bot.reply_to(message, response, parse_mode="HTML")

        self.stdout.write(
            self.style.SUCCESS("Бот запущений... Спробуй написати /list у Telegram")
        )
        bot.polling(none_stop=True)
