from django.contrib import admin
from .models import EstadoCuentaModel

@admin.register(EstadoCuentaModel)
class EstadoCuentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)
    list_filter = ('nombre',)
    ordering = ('id',)
    fields = ('nombre',)