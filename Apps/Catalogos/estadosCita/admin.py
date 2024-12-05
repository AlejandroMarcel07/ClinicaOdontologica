from django.contrib import admin
from .models import EstadoCitaModel

@admin.register(EstadoCitaModel)
class EstadoCitaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')  #
    search_fields = ('nombre',)
    list_filter = ('nombre',)
    ordering = ('id',)
    fields = ('nombre',)