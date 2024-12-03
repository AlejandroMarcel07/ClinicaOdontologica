from django.urls import path, include

urlpatterns = [
    path('usuarios/', include('Apps.Seguridad.usuarios.urls')),
]