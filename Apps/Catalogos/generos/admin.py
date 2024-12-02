from django.contrib import admin
from .models import GeneroModel

@admin.register(GeneroModel)
class GeneroAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')  #
    search_fields = ('nombre',)
    list_filter = ('nombre',)
    ordering = ('id',)
    fields = ('nombre',)