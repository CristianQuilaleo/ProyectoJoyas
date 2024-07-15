$(document).ready(function () {
    $(".btn-add-cart").click(function () {
        var productId = $(this).data("id");
        $.ajax({
            url: "/add-to-cart/",
            method: "POST",
            data: {
                'product_id': productId,
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function (response) {
                alert(response.message);
                updateCartCount(response.cart_count);
            },
            error: function (error) {
                alert("Error al añadir el producto al carrito");
            }
        });
    });

    $(".btn-remove-cart").click(function () {
        var productId = $(this).data("id");
        $.ajax({
            url: "/remove-from-cart/",
            method: "POST",
            data: {
                'product_id': productId,
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function (response) {
                alert(response.message);
                updateCartCount(response.cart_count);
                // Optionally, remove the item from the cart UI
                $("#cart-item-" + productId).remove();
            },
            error: function (error) {
                alert("Error al eliminar el producto del carrito");
            }
        });
    });

    function updateCartCount(count) {
        $("#cart-count").text(count);
    }
});