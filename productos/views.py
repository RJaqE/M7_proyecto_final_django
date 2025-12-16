from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Producto, Categoria, Etiqueta, DetalleProducto
from .forms import ProductoForm, DetalleProductoForm, CategoriaForm, EtiquetaForm

# --- VISTA PRINCIPAL ---
def index(request):
    return render(request, 'productos/index.html')

# --- GESTIÓN DE PRODUCTOS ---

def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos/lista_productos.html', {'productos': productos})

@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        detalle_form = DetalleProductoForm(request.POST)
        
        if form.is_valid() and detalle_form.is_valid():
            # 1. Guarda el producto
            producto = form.save()
            
            # 2. Guarda el detalle pero sin enviarlo a la BD aún (commit=False)
            detalle = detalle_form.save(commit=False)
            # 3. Asigna el ID del producto recién creado al detalle
            detalle.producto = producto
            # 4. Guarda el detalle
            detalle.save()
            
            messages.success(request, 'Producto creado correctamente.')
            return redirect('lista_productos')
    else:
        form = ProductoForm()
        detalle_form = DetalleProductoForm()
    
    return render(request, 'productos/producto_form.html', {
        'form': form, 
        'detalle_form': detalle_form,
        'titulo': 'Crear Producto'
    })

@login_required
def detalle_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    return render(request, 'productos/producto_detalle.html', {'producto': producto})

@login_required
def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    
    # Intentamos obtener los detalles, si no existen (creados por admin simple), manejamos el error
    try:
        detalle = producto.detalles
    except DetalleProducto.DoesNotExist:
        detalle = None

    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        detalle_form = DetalleProductoForm(request.POST, instance=detalle)
        
        if form.is_valid() and detalle_form.is_valid():
            producto = form.save()
            detalle = detalle_form.save(commit=False)
            detalle.producto = producto
            detalle.save()
            messages.success(request, 'Producto actualizado correctamente.')
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=producto)
        detalle_form = DetalleProductoForm(instance=detalle)

    return render(request, 'productos/producto_form.html', {
        'form': form, 
        'detalle_form': detalle_form,
        'titulo': 'Editar Producto'
    })

@login_required
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado.')
        return redirect('lista_productos')
    return render(request, 'productos/producto_confirmar_eliminar.html', {'producto': producto})

# --- GESTIÓN DE CATEGORÍAS ---

def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'productos/categoria_lista.html', {'categorias': categorias})

@login_required
def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada.')
            return redirect('lista_categorias')
    else:
        form = CategoriaForm()
    return render(request, 'productos/categoria_form.html', {'form': form, 'titulo': 'Nueva Categoría'})

@login_required
def editar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría actualizada.')
            return redirect('lista_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'productos/categoria_form.html', {'form': form, 'titulo': 'Editar Categoría'})

@login_required
def eliminar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoría eliminada.')
        return redirect('lista_categorias')
    return render(request, 'productos/categoria_confirmar_eliminar.html', {'objeto': categoria, 'tipo': 'Categoría'})

# --- GESTIÓN DE ETIQUETAS ---

def lista_etiquetas(request):
    etiquetas = Etiqueta.objects.all()
    return render(request, 'productos/etiqueta_lista.html', {'etiquetas': etiquetas})

@login_required
def crear_etiqueta(request):
    if request.method == 'POST':
        form = EtiquetaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Etiqueta creada.')
            return redirect('lista_etiquetas')
    else:
        form = EtiquetaForm()
    return render(request, 'productos/etiqueta_form.html', {'form': form, 'titulo': 'Nueva Etiqueta'})

@login_required
def editar_etiqueta(request, id):
    etiqueta = get_object_or_404(Etiqueta, id=id)
    if request.method == 'POST':
        form = EtiquetaForm(request.POST, instance=etiqueta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Etiqueta actualizada.')
            return redirect('lista_etiquetas')
    else:
        form = EtiquetaForm(instance=etiqueta)
    return render(request, 'productos/etiqueta_form.html', {'form': form, 'titulo': 'Editar Etiqueta'})

@login_required
def eliminar_etiqueta(request, id):
    etiqueta = get_object_or_404(Etiqueta, id=id)
    if request.method == 'POST':
        etiqueta.delete()
        messages.success(request, 'Etiqueta eliminada.')
        return redirect('lista_etiquetas')
    return render(request, 'productos/categoria_confirmar_eliminar.html', {'objeto': etiqueta, 'tipo': 'Etiqueta'})


# -- REPORTES AVANZADOS --

@login_required
def ver_reportes(request):
    # 1. ORM: Filtro avanzado (Precio mayor a 50 - ajusta el valor según tus datos)
    productos_caros = Producto.objects.filter(precio__gt=50)

    # 2. ORM: Uso de exclude (Todos los productos MENOS los de 'Hogar' - ajusta el nombre)
    # Nota: Usamos 'categoria__nombre' para filtrar por el campo nombre de la relación
    productos_sin_hogar = Producto.objects.exclude(categoria__nombre='Hogar')

    # 3. SQL Personalizado (Raw SQL)
    # Consultamos productos directamente con SQL. 
    # Es útil para reportes complejos que el ORM no soporta bien.
    consulta_sql = "SELECT * FROM productos_producto WHERE precio < 50"
    productos_baratos_sql = Producto.objects.raw(consulta_sql)

    return render(request, 'productos/reportes.html', {
        'productos_caros': productos_caros,
        'productos_sin_hogar': productos_sin_hogar,
        'productos_baratos_sql': productos_baratos_sql,
    })