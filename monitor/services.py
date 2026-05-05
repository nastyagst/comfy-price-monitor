import os
import httpx
from bs4 import BeautifulSoup
from decimal import Decimal
from monitor.models import Product, PriceAlert
from dotenv import load_dotenv

load_dotenv()


def update_product_price(product_id):
    product = Product.objects.get(id=product_id)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }

    try:
        with httpx.Client(
            headers=headers, follow_redirects=True, timeout=15.0
        ) as client:
            response = client.get(product.url)

            if response.status_code != 200 and len(response.text) < 5000:
                return False

            soup = BeautifulSoup(response.text, "html.parser")

            # Шукаємо ціну для Brain, Comfy або ITbox
            price_element = (
                soup.find("span", class_="price-number")
                or soup.find("div", class_="price__current")
                or soup.find("div", class_="price")
            )

            if price_element:
                raw_price = price_element.get_text(strip=True)
                clean_price = "".join(filter(str.isdigit, raw_price))

                if clean_price:
                    product.current_price = Decimal(clean_price)
                    title_element = soup.find("h1")
                    if title_element:
                        product.title = title_element.get_text(strip=True)
                    product.save()
                    return True
    except Exception as e:
        print(f"Error parsing: {e}")
    return False


def get_user_alerts_list():
    alerts = PriceAlert.objects.filter(is_active=True)
    if not alerts.exists():
        return "У тебе поки немає активних підписок."

    response = "<b>Твій список моніторингу:</b>\n\n"
    for alert in alerts:
        response += (
            f"📍 {alert.product.title}\n"
            f"Ціна зараз: {alert.product.current_price} грн\n"
            f"Цільова: {alert.target_price} грн\n"
            f"<a href='{alert.product.url}'>Посилання</a>\n"
            f"-------------------\n"
        )
    return response


def send_telegram_notification(title, old_price, new_price, url):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("MY_CHAT_ID")
    message = (
        f"📉 <b>Ціна впала!</b>\n\n"
        f"Товар: {title}\n"
        f"Стара ціна: {old_price} грн\n"
        f"Нова ціна: <b>{new_price} грн</b>\n\n"
        f"<a href='{url}'>Купити</a>"
    )
    api_url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
    with httpx.Client() as client:
        client.post(api_url, json=payload)
