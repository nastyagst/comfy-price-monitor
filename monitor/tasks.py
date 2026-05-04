from celery import shared_task
from monitor.models import PriceAlert
from monitor.services import update_product_price, send_telegram_notification


@shared_task
def update_all_products_prices():
    active_alerts = PriceAlert.objects.filter(is_active=True)

    for alert in active_alerts:
        product = alert.product
        old_price = product.current_price

        if update_product_price(product.id):
            product.refresh_from_db()
            new_price = product.current_price

            if new_price and old_price and new_price < old_price:
                if new_price <= alert.target_price:
                    send_telegram_notification(
                        product.title, old_price, new_price, product.url
                    )

    return f"Processed {active_alerts.count()} alerts"
