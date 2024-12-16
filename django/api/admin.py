from django.contrib import admin
from .models import *

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Captura)
admin.site.register(Categoria)
admin.site.register(Muestra)
admin.site.register(Lote)
admin.site.register(Organo)
admin.site.register(Sistema)
admin.site.register(Notas)