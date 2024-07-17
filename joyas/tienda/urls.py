from django.contrib import admin
from django.urls import path, include
from . import views
from .views import add_to_cart, remove_from_cart, registro, exit

urlpatterns = [
    path('', views.home, name='home'),
    path('carrito/', views.carrito, name='carrito'),
    path('inicio_sesion/', views.inicio_sesion, name='inicio_sesion'),
    path('registro/', views.registro, name='registro'),
    path('articulo/', views.base, name='base'),
    path('confirmar-pedido/', views.confirmar_pedido, name='confirmar_pedido'),
    path('add-to-cart/<int:producto_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:pedido_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('admin_productos/', views.admin_productos, name='admin_productos'),
    path('agregar_producto/', views.agregar_producto, name='agregar_producto'),
    path('editar_producto/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('eliminar_producto/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', exit, name='exit'),

]
