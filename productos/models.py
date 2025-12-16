from django.db import models

# 1. Modelo Categoría (Independiente)
# Relación: Una categoría puede tener muchos productos.
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    
    class Meta:
        verbose_name_plural = "Categorías" 

    def __str__(self):
        return self.nombre

# 2. Modelo Etiqueta
# Relación: Muchos a Muchos con Producto 
class Etiqueta(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

# 3. Modelo Producto 
class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(verbose_name="Descripción")
    # Usa DecimalField para dinero para evitar errores de redondeo de los floats
    precio = models.DecimalField(max_digits=10, decimal_places=2) 
    
    # Relación Muchos a Uno: Un producto tiene UNA categoría.
    # on_delete=models.CASCADE significa que si borras la categoría, se borran sus productos.
    # (Podrías usar models.PROTECT si prefieres evitar eso).
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    
    # Relación Muchos a Muchos: Un producto puede tener muchas etiquetas.
    etiquetas = models.ManyToManyField(Etiqueta, blank=True) 

    def __str__(self):
        return self.nombre

# 4. Modelo DetalleProducto (Relación Uno a Uno)
# Esto separa datos técnicos del producto principal.
class DetalleProducto(models.Model):
    # OneToOneField asegura que un producto solo tenga un set de detalles
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE, related_name='detalles')
    peso = models.DecimalField(max_digits=5, decimal_places=2, help_text="Peso en kg")
    dimensiones = models.CharField(max_length=100, help_text="Ej: 30x20x10 cm")
    fecha_fabricacion = models.DateField(null=True, blank=True) 

    def __str__(self):
        return f"Detalles de {self.producto.nombre}"