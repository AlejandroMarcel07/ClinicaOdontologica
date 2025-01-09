from django.urls import path, include

urlpatterns = [
    path('genero/', include('Apps.Catalogos.generos.urls')),
    path('estadoCita/', include('Apps.Catalogos.estadosCita.urls')),
    path('estadoCuenta/', include('Apps.Catalogos.estadosCuenta.urls')),
    path('tipoPago/', include('Apps.Catalogos.tiposPago.urls')),
    path('frecuencia/', include('Apps.Catalogos.frecuencias.urls')),
    path('periocidad/', include('Apps.Catalogos.periocidades.urls')),
    path('tratamiento/', include('Apps.Catalogos.tratamientos.urls')),
    path('exploracion/', include('Apps.Catalogos.exploraciones.urls')),
    path('estadoFecha/', include('Apps.Catalogos.estadosFecha.urls')),
    path('estadoPago/', include('Apps.Catalogos.estadosPago.urls')),
]