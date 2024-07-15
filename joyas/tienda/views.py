from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Producto, Carrito, Pedido
from .forms import ProductoForm

def home(request):
    productos = Producto.objects.all()
    return render(request, 'home.html', {'productos': productos})

@login_required
def carrito(request):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    pedidos = Pedido.objects.filter(carrito=carrito)
    return render(request, 'carrito.html', {'carrito': carrito, 'pedidos': pedidos})

@login_required
def add_to_cart(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    pedido, created = Pedido.objects.get_or_create(carrito=carrito, producto=producto)

    if not created:
        pedido.cantidad += 1
    pedido.save()

    messages.success(request, 'Producto agregado al carrito.')
    return redirect('base')

@login_required
def remove_from_cart(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        producto = get_object_or_404(Producto, id=product_id)
        carrito = Carrito.objects.get(usuario=request.user)
        
        pedido = Pedido.objects.get(carrito=carrito, producto=producto)
        if pedido.cantidad > 1:
            pedido.cantidad -= 1
            pedido.save()
        else:
            pedido.delete()
        
        messages.success(request, f'{producto.nombre} ha sido eliminado del carrito')
        return redirect('carrito')
    
    # Si el método no es POST, retornar un error
    messages.error(request, 'Método no permitido')
    return redirect('home')

def inicio_sesion(request):
    return render(request, 'InicioSesion.html')

def registro(request):
    return render(request, 'Registro.html')

def base(request):
    productos = Producto.objects.all()
    return render(request, 'base.html', {'productos': productos})

def confirmar_pedido(request):
    return render(request, 'confirmarPedido.html')


def admin_productos(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_productos')
    else:
        form = ProductoForm()
    return render(request, 'admin_productos.html', {'form': form})

def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto agregado exitosamente')
            return redirect('admin_productos')
    else:
        form = ProductoForm()
    return render(request, 'admin_productos.html', {'form': form})

def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado exitosamente')
            return redirect('admin_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'admin_productos.html', {'form': form, 'producto': producto})

def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.delete()
    messages.success(request, 'Producto eliminado exitosamente')
    return redirect('admin_productos')