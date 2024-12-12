from django.urls import path
from .views import TipoPagoApiView

urlpatterns = [
    path("", TipoPagoApiView.as_view(), name="tipos"),
    path("id/<int:id>/", TipoPagoApiView.as_view(), name="tipos-patch"),
]