from django.urls import path
from .views import TratamientoApiView

urlpatterns = [
    path("", TratamientoApiView.as_view(), name="tratamientos"),
    path("id/<int:id>/", TratamientoApiView.as_view(), name="tratamientos-patch"),
]