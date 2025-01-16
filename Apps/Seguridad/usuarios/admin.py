from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from Apps.Seguridad.usuarios.models import User
@admin.register(User)
class UsuariosAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Informacion de la clinica', {'fields': ('clinica',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informacion de la clinica', {'fields': ('clinica',)}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'clinica')
    list_filter = ('clinica',)
    search_fields = ('username', 'email', 'clinica__nombre')