from django.contrib import admin
from monitor.models import Product, PriceAlert
from monitor.services import update_product_price


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "current_price", "last_updated")
    search_fields = ("title", "url")
    actions = ["refresh_prices"]

    @admin.display(description="Оновити ціни вибраних товарів")
    def refresh_prices(self, request, queryset):
        success_count = 0
        for product in queryset:
            if update_product_price(product.id):
                success_count += 1

        self.message_user(request, f"Оновлено товарів: {success_count}")


@admin.register(PriceAlert)
class PriceAlertAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "target_price", "is_active")
