from django.contrib import admin
from .models import Editorial, Comic
from .utils import formato_pesos


@admin.register(Editorial)
class EditorialAdmin(admin.ModelAdmin):
    search_fields = ('nombre',)


@admin.register(Comic)
class ComicAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'editorial', 'tomo', 'stock', 'precio_clp', 'tapa_dura', 'disponible')
    list_filter = ('editorial', 'tapa_dura')
    search_fields = ('titulo',)

    @admin.display(description='Precio', ordering='precio')
    def precio_clp(self, obj):
        return formato_pesos(obj.precio)