from django.contrib import admin
from .models import TipoPagoModel

@admin.register(TipoPagoModel)
class TipoPagoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)
    list_filter = ('nombre',)
    ordering = ('id',)
    fields = ('nombre',)