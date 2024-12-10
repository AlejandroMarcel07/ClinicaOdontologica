from django.urls import path, include

urlpatterns = [
    path('genero/', include('Apps.Catalogos.generos.urls')),
    path('estadoCita/', include('Apps.Catalogos.estadosCita.urls')),
    path('estadoCuenta/', include('Apps.Catalogos.estadosCuenta.urls')),
]