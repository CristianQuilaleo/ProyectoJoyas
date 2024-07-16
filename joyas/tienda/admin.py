from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Producto, Pedido,  Carrito, ItemCarrito

admin.site.register(Producto)
admin.site.register(Pedido)
admin.site.register(Carrito)
admin.site.register(ItemCarrito)

