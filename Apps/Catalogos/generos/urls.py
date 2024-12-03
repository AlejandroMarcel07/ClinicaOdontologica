from django.urls import path
from .views import GeneroApiView

urlpatterns = [
    path("", GeneroApiView.as_view(), name="generos"),
]