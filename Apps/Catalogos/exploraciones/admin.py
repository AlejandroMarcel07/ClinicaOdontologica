from django.contrib import admin
from .models import ExploracionModel

@admin.register(ExploracionModel)
class ExploracionAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)
    list_filter = ('nombre',)
    ordering = ('id',)
    fields = ('nombre',)