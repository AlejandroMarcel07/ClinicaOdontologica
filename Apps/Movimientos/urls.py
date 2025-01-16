from django.urls import path, include

urlpatterns = [
    path('clinica/', include('Apps.Movimientos.clinicas.urls')),
]