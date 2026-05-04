from django.contrib import admin
from models import Product, PriceAlert


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "current_price", "last_updated")
    search_fields = ("title", "url")


@admin.register(PriceAlert)
class PriceAlertAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "target_price", "is_active")
    list_filter = ("is_active",)
