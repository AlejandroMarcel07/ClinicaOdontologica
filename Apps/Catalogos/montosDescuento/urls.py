from django.urls import path
from .views import MontoDescuentoApiView

urlpatterns = [
    path("", MontoDescuentoApiView.as_view(), name="montosDescuento"),
    path("id/<int:id>/", MontoDescuentoApiView.as_view(), name="montosDescuento-patch"),
]