from django.contrib import admin
from .models import ModalidadPagoModel

@admin.register(ModalidadPagoModel)
class ModalidadPagoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)
    list_filter = ('nombre',)
    ordering = ('id',)
    fields = ('nombre',)