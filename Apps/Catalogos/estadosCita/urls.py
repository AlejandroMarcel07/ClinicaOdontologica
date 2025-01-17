from django.urls import path
from .views import EstadoCitaApiView

urlpatterns = [
    path("", EstadoCitaApiView.as_view(), name="estadosCita"),
    path("id/<int:id>/", EstadoCitaApiView.as_view(), name="estados-patch"),
]