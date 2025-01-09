from django.contrib import admin
from .models import EstadoFechaModel

@admin.register(EstadoFechaModel)
class EstadoFechaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)
    list_filter = ('nombre',)
    ordering = ('id',)
    fields = ('nombre',)