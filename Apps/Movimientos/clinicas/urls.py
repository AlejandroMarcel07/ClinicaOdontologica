from django.urls import path
from .views import ClinicaApiView

urlpatterns = [
    path("", ClinicaApiView.as_view(), name="clinicas"),
    path("id/<int:id>/", ClinicaApiView.as_view(), name="clinicas-patch"),
]