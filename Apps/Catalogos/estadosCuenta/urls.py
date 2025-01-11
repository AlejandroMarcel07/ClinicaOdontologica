from django.urls import path
from .views import EstadoCuentaApiView

urlpatterns = [
    path("", EstadoCuentaApiView.as_view(), name="estadosCuenta"),
    path("id/<int:id>/", EstadoCuentaApiView.as_view(), name="estados-patch"),
]