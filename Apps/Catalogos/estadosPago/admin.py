from django.contrib import admin
from .models import EstadoPagoModel

@admin.register(EstadoPagoModel)
class EstadoPagoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)
    list_filter = ('nombre',)
    ordering = ('id',)
    fields = ('nombre',)