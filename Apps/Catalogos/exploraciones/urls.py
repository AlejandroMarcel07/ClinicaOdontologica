from django.urls import path
from .views import ExploracionApiView

urlpatterns = [
    path("", ExploracionApiView.as_view(), name="exploraciones"),
    path("id/<int:id>/", ExploracionApiView.as_view(), name="exploraciones-patch"),
]