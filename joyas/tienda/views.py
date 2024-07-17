from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Producto, Carrito, Pedido
from .forms import ProductoForm, CustomUserCreationForm
from django.db.models import Sum
from django.contrib.auth import authenticate, login, logout


def home(request):
    productos = Producto.objects.all()
    return render(request, 'home.html', {'productos': productos})


def carrito(request):
    if request.user.is_authenticated:
        carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    else:
        carrito_id = request.session.get('carrito_id')
        if carrito_id:
            carrito = Carrito.objects.get(id=carrito_id)
        else:
            carrito = Carrito.objects.create()
            request.session['carrito_id'] = carrito.id

    pedidos_en_carrito = carrito.pedido_set.all()  # Obtener todos los pedidos del carrito
    total = pedidos_en_carrito.aggregate(Sum('total'))['total__sum'] or 0  # Calcular el total del carrito
    
    return render(request, 'carrito.html', {'carrito': pedidos_en_carrito, 'total': total})


def add_to_cart(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    if request.user.is_authenticated:
        carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    else:
        carrito_id = request.session.get('carrito_id')
        if carrito_id:
            carrito = Carrito.objects.get(id=carrito_id)
        else:
            carrito = Carrito.objects.create()
            request.session['carrito_id'] = carrito.id

    pedido, created = Pedido.objects.get_or_create(carrito=carrito, producto=producto)
    if not created:
        pedido.cantidad += 1
        pedido.save()
    
    messages.success(request, f'El producto "{producto.nombre}" ha sido agregado al carrito.')
    return redirect('base')

def remove_from_cart(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    if request.user.is_authenticated:
        carrito = Carrito.objects.get(usuario=request.user)
    else:
        carrito_id = request.session.get('carrito_id')
        if carrito_id:
            carrito = Carrito.objects.get(id=carrito_id)
        else:
            carrito = None
    
    if carrito:
        pedido = Pedido.objects.filter(carrito=carrito, producto=producto).first()
        if pedido:
            if pedido.cantidad > 1:
                pedido.cantidad -= 1
                pedido.save()
            else:
                pedido.delete()
            messages.success(request, f'El producto "{producto.nombre}" ha sido eliminado del carrito.')
        else:
            messages.info(request, f'El producto "{producto.nombre}" no estaba en el carrito.')
    
    return redirect('base')

def base(request):
    productos = Producto.objects.all()
    return render(request, 'base.html', {'productos': productos})

def inicio_sesion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Usuario logueado con éxito')
            return redirect('home')  # Redirige a una vista específica después de iniciar sesión
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos')
    return render(request, 'InicioSesion.html')

def registro(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        user_creation_form = CustomUserCreationForm(data=request.POST)

        if user_creation_form.is_valid():
            user_creation_form.save()

            user = authenticate(username=user_creation_form.cleaned_data['username'], password=user_creation_form.cleaned_data['password1'])
            login(request, user)
            messages.success(request, 'Usuario registrado y logueado exitosamente')
            return redirect('home')

    return render(request, 'Registro.html', data)

def exit(request):
    logout(request)
    return redirect('home')

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