from django.contrib import admin
from .models import PacienteModel

@admin.register(PacienteModel)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'cedula', 'nombre', 'edad', 'genero', 'direccion', 'ocupacion', 'isdeleted')
    search_fields = ('cedula','nombre')
    list_filter = ('cedula','nombre',)
    ordering = ('id',)
    fields = ('cedula', 'nombre', 'edad', 'genero', 'direccion', 'ocupacion', 'isdeleted')