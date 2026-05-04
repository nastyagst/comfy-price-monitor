from rest_framework import serializers
from monitor.models import Product, PriceAlert


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title", "url", "current_price", "last_updated"]
        read_only_fields = ["title", "current_price", "last_updated"]


class PriceAlertSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_url = serializers.URLField(write_only=True)
    target_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False
    )

    class Meta:
        model = PriceAlert
        fields = ["id", "product", "product_url", "target_price", "is_active"]
