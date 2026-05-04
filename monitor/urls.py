from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PriceAlertViewSet

router = DefaultRouter()
router.register(r"alerts", PriceAlertViewSet, basename="pricealert")

urlpatterns = [path("", include(router.urls))]
