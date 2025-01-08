from django.urls import path
from .views import FrecuenciaApiView

urlpatterns = [
    path("", FrecuenciaApiView.as_view(), name="frecuencias"),
    path("id/<int:id>/", FrecuenciaApiView.as_view(), name="frecuencias-patch"),
]