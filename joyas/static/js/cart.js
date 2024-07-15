// Script para manejar el carrito de compras
document.addEventListener('DOMContentLoaded', function() {
    const btnAgregarCarrito = document.querySelectorAll('.btn-agregar-carrito');

    btnAgregarCarrito.forEach(btn => {
        btn.addEventListener('click', agregarAlCarrito);
    });

    function agregarAlCarrito(event) {
        const producto = event.target.closest('.producto');
        const productoId = producto.dataset.productoId;
        const nombre = producto.querySelector('.producto-nombre').textContent;
        const precio = parseFloat(producto.querySelector('.producto-precio').textContent.replace('$', ''));

        const item = {
            id: productoId,
            nombre: nombre,
            precio: precio,
            cantidad: 1
        };

        if (localStorage.getItem('carrito') === null) {
            const carrito = [];
            carrito.push(item);
            localStorage.setItem('carrito', JSON.stringify(carrito));
        } else {
            let carrito = JSON.parse(localStorage.getItem('carrito'));
            const encontrado = carrito.some(prod => prod.id === item.id);
            if (!encontrado) {
                carrito.push(item);
            } else {
                carrito = carrito.map(prod => {
                    if (prod.id === item.id) {
                        prod.cantidad += 1;
                    }
                    return prod;
                });
            }
            localStorage.setItem('carrito', JSON.stringify(carrito));
        }

        actualizarCarrito();
    }

    function actualizarCarrito() {
        const carrito = JSON.parse(localStorage.getItem('carrito'));
        const carritoLista = document.getElementById('carrito-lista');

        if (carritoLista !== null) {
            carritoLista.innerHTML = '';
            let total = 0;

            carrito.forEach(item => {
                const subtotal = item.precio * item.cantidad;
                total += subtotal;

                const itemHTML = `
                    <div class="carrito-item">
                        <span>${item.nombre} - Cantidad: ${item.cantidad}</span>
                        <span class="float-right">$${subtotal.toFixed(2)}</span>
                    </div>
                `;
                carritoLista.innerHTML += itemHTML;
            });

            const totalHTML = `
                <div class="carrito-total">
                    <span>Total: </span>
                    <span class="float-right">$${total.toFixed(2)}</span>
                </div>
            `;
            carritoLista.innerHTML += totalHTML;
        }
    }
});
