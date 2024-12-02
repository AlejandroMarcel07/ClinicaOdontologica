from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from Apps.Seguridad.usuarios.models import User
@admin.register(User)
class UsuariosAdmin(UserAdmin):
    pass