from django.urls import path
from .views import PeriocidadApiView

urlpatterns = [
    path("", PeriocidadApiView.as_view(), name="periocidades"),
    path("id/<int:id>/", PeriocidadApiView.as_view(), name="periocidades-patch"),
]