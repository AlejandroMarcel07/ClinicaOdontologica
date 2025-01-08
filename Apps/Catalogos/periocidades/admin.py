from django.contrib import admin
from .models import PeriocidadModel

@admin.register(PeriocidadModel)
class PeriocidadAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)
    list_filter = ('nombre',)
    ordering = ('id',)
    fields = ('nombre',)