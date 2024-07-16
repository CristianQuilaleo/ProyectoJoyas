from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Producto, Carrito, Pedido
from .forms import ProductoForm
from django.db.models import Sum


def home(request):
    productos = Producto.objects.all()
    return render(request, 'home.html', {'productos': productos})


def carrito(request):
    if request.user.is_authenticated:
        carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    else:
        carrito_id = request.session.get('carrito_id')
        carrito, created = Carrito.objects.get_or_create(id=carrito_id)
    
    pedidos_en_carrito = carrito.pedido_set.all()  # Obtener todos los pedidos del carrito
    total = pedidos_en_carrito.aggregate(Sum('total'))['total__sum'] or 0  # Calcular el total del carrito
    
    # Obtener todos los productos del carrito
    productos_en_carrito = [pedido.producto for pedido in pedidos_en_carrito]
    
    return render(request, 'carrito.html', {'carrito': pedidos_en_carrito, 'productos': productos_en_carrito, 'total': total})

def add_to_cart(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    if 'cart' not in request.session:
        request.session['cart'] = []
    
    cart = request.session['cart']
    
    if producto_id not in cart:
        cart.append(producto_id)
        request.session['cart'] = cart
        messages.success(request, f'El producto "{producto.nombre}" ha sido agregado al carrito.')
    
    return redirect('base')


def remove_from_cart(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    if 'cart' in request.session:
        cart = request.session['cart']
        
        if producto_id in cart:
            cart.remove(producto_id)
            request.session['cart'] = cart
            messages.success(request, f'El producto "{producto.nombre}" ha sido eliminado del carrito.')
        else:
            messages.info(request, f'El producto "{producto.nombre}" no estaba en el carrito.')
    
    return redirect('base')

def base(request):
    productos = Producto.objects.all()
    return render(request, 'base.html', {'productos': productos})

def inicio_sesion(request):
    return render(request, 'InicioSesion.html')

def registro(request):
    return render(request, 'Registro.html')

@login_required
def confirmar_pedido(request):
    if request.method == 'POST':
        # Aquí puedes manejar la lógica de confirmación de la compra
        pedidos = Pedido.objects.filter(usuario=request.user)
        # Procesar la compra...
        return render(request, 'confirmarPedido.html', {'pedidos': pedidos})
    else:
        return redirect('carrito')
    


def admin_productos(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto agregado exitosamente')
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

def cart_detail(request):
    if request.user.is_authenticated:
        carrito = Carrito.objects.filter(usuario=request.user).first()
    else:
        carrito_id = request.session.get('carrito_id')
        carrito = Carrito.objects.filter(id=carrito_id).first() if carrito_id else None

    return render(request, 'carrito.html', {'carrito': carrito})