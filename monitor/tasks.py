from celery import shared_task

from monitor.models import Product
from monitor.services import update_product_price


@shared_task
def update_all_products_prices():
    active_products = Product.objects.filter(alerts__is_active=True).distinct()

    for product in active_products:
        update_product_price(product.id)

    return f"Updated {active_products.count()} products"
