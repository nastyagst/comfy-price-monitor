from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Product(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField(unique=True)
    current_price = models.DecimalField(
        max_digits=2,
        decimal_places=2,
        null=True,
        blank=True,
    )
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class PriceAlert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="alerts")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="alerts"
    )
    target_price = models.DecimalField(max_digits=2, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("user", "product")

    def __str__(self):
        return f"{self.user.username} стежить за {self.product.title}"
