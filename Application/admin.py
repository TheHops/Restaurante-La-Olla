from django.contrib import admin
from Application.models import *
from django.contrib.auth.admin import UserAdmin

admin.site.register(Platillo)
admin.site.register(AreaMesa)
admin.site.register(Cargo)
admin.site.register(DetalleOrden)
admin.site.register(Orden)
admin.site.register(Mesa)
admin.site.register(TipoPlatillo)

class CustomUserAdmin(UserAdmin):
    model = Usuario

admin.site.register(Usuario, CustomUserAdmin)


# Register your models here.
