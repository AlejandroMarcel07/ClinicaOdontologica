from django.contrib import admin
from .models import ClinicaModel

@admin.register(ClinicaModel)
class ClinicaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'direccion', 'telefono', 'encargado')
    search_fields = ('nombre','encargado')
    list_filter = ('nombre',)
    ordering = ('id',)
    fields = ('nombre',)