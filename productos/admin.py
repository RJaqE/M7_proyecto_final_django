from django.contrib import admin
from .models import Categoria, Etiqueta, Producto, DetalleProducto


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(Etiqueta)
class EtiquetaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

# Permite editar los Detalles DENTRO de la pantalla de Producto (Inline)
class DetalleProductoInline(admin.StackedInline):
    model = DetalleProducto
    can_delete = False
    verbose_name_plural = 'Detalles del Producto'

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio') # Columnas visibles en la lista
    list_filter = ('categoria', 'etiquetas')        # Filtros laterales
    search_fields = ('nombre', 'descripcion')       # Barra de búsqueda
    inlines = [DetalleProductoInline]               # Agrega el formulario de detalles aquí mismo

# El modelo DetalleProducto no necesita registrarse por separado si usamos el Inline arriba,
# pero si quieres verlo suelto, puedes descomentar la siguiente línea:
# admin.site.register(DetalleProducto)