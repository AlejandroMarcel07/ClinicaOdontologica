from django.urls import path, include

urlpatterns = [
    path('genero/', include('Apps.Catalogos.generos.urls')),
]