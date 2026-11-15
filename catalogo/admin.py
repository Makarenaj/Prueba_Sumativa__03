from django.contrib import admin
from .models import Editorial, Comic, Reserva
from .utils import formato_pesos
from django.utils.html import format_html


@admin.register(Editorial)
class EditorialAdmin(admin.ModelAdmin):
    search_fields = ('nombre',)

@admin.register(Comic)
class ComicAdmin(admin.ModelAdmin):
    list_display = ('miniatura', 'titulo', 'editorial', 'tomo', 'stock', 'precio_clp', 'tapa_dura', 'disponible')
    list_filter = ('editorial', 'tapa_dura')
    search_fields = ('titulo',)

    @admin.display(description='Precio', ordering='precio')
    def precio_clp(self, obj):
        return formato_pesos(obj.precio)

    @admin.display(description='Portada')
    def miniatura(self, obj):
        return format_html(
        '<img src="{}" style="height:60px; border-radius:4px;">',
        obj.portada.url
        )

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'comic', 'nombre', 'rut', 'cantidad', 'fecha')
    list_filter = ('comic',)
    search_fields = ('nombre', 'rut')
