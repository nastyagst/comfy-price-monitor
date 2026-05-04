from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from .models import Product, PriceAlert
from .serializers import PriceAlertSerializer
from .services import update_product_price


class PriceAlertViewSet(viewsets.ModelViewSet):
    serializer_class = PriceAlertSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PriceAlert.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        url = request.data.get("product_url")
        target_price = request.data.get("target_price")
        product, created = Product.objects.get_or_create(url=url)

        if created:
            update_product_price(product.id)
            product.refresh_from_db()

        alert, alert_created = PriceAlert.objects.get_or_create(
            user=request.user, product=product, defaults={"target_price": target_price}
        )
        serializer = self.get_serializer(alert)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
