from django.urls import path
from .views import EstadoPagoApiView

urlpatterns = [
    path("", EstadoPagoApiView.as_view(), name="estadosPago"),
    path("id/<int:id>/", EstadoPagoApiView.as_view(), name="estadosPago-patch"),
]