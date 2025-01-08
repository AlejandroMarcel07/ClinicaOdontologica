from django.contrib import admin
from .models import FrecuenciaModel

@admin.register(FrecuenciaModel)
class FrecuenciaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)
    list_filter = ('nombre',)
    ordering = ('id',)
    fields = ('nombre',)