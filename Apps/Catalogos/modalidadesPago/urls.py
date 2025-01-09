from django.urls import path
from .views import ModalidadPagoApiView

urlpatterns = [
    path("", ModalidadPagoApiView.as_view(), name="modalidadPago"),
    path("id/<int:id>/", ModalidadPagoApiView.as_view(), name="modalidadPago-patch"),
]