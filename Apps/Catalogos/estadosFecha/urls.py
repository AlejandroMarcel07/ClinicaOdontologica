from django.urls import path
from .views import EstadoFechaApiView

urlpatterns = [
    path("", EstadoFechaApiView.as_view(), name="estados"),
    path("id/<int:id>/", EstadoFechaApiView.as_view(), name="estados-patch"),
]