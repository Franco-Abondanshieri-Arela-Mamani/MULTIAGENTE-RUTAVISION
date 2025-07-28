from django.contrib import admin
from .models import Obstaculo, RutaSimple

@admin.register(Obstaculo)
class ObstaculoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'latitud', 'longitud')
    search_fields = ('nombre', 'tipo')

@admin.register(RutaSimple)
class RutaSimpleAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'color', 'descripcion')
    search_fields = ('nombre',)
