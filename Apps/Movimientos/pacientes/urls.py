from django.urls import path
from .views import PacienteApiView

urlpatterns = [
    path("", PacienteApiView.as_view(), name="pacientes"),
    path("id/<int:id>/", PacienteApiView.as_view(), name="pacientes-patch"),
]