import telebot
from django.core.management.base import BaseCommand
from django.conf import settings
from monitor.services import get_user_alerts_list, update_product_price
from monitor.models import Product, PriceAlert


class Command(BaseCommand):
    help = "Starts the telegram bot"

    def handle(self, *args, **options):
        bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)

        @bot.message_handler(commands=["start"])
        def start_handler(message):
            bot.reply_to(
                message,
                "Привіт! Я твій монітор цін. Напиши /list для списку або скинь посилання на товар (Brain, ITbox, Comfy).",
            )

        @bot.message_handler(commands=["list"])
        def list_alerts(message):
            response = get_user_alerts_list()
            bot.reply_to(message, response, parse_mode="HTML")

        @bot.message_handler(
            func=lambda message: message.text and message.text.startswith("http")
        )
        def add_alert(message):
            url = message.text.strip()
            bot.reply_to(message, "🔍 Перевіряю товар...")

            product, _ = Product.objects.get_or_create(url=url)
            success = update_product_price(product.id)

            if success:
                product.refresh_from_db()
                PriceAlert.objects.get_or_create(
                    product=product, defaults={"target_price": product.current_price}
                )

                msg = (
                    f"✅ <b>Додано!</b>\n\n"
                    f"Назва: {product.title}\n"
                    f"Ціна: {product.current_price} грн\n\n"
                    f"Стежу за змінами."
                )
                bot.reply_to(message, msg, parse_mode="HTML")
            else:
                bot.reply_to(
                    message,
                    "❌ Не вдалося отримати дані. Можливо, сайт захищений або посилання невірне.",
                )

        self.stdout.write(self.style.SUCCESS("Бот запущений..."))
        bot.polling(none_stop=True)
