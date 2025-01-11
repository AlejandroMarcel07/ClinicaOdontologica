from django.contrib import admin
from .models import MontoDescuentoModel

@admin.register(MontoDescuentoModel)
class MontoDescuentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cantidad')
    search_fields = ('cantidad',)
    list_filter = ('cantidad',)
    ordering = ('id',)
    fields = ('cantidad',)
