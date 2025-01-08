from django.contrib import admin
from .models import TratamientoModel

@admin.register(TratamientoModel)
class TratamientoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)
    list_filter = ('nombre',)
    ordering = ('id',)
    fields = ('nombre',)