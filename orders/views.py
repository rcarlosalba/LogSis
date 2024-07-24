from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart, CartItem, Order, OrderItem
from inventory.models import Product


@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        action = request.POST.get('action')
        if item_id and action:
            try:
                item = CartItem.objects.get(id=item_id, cart=cart)
                if action == 'increase':
                    item.quantity += 1
                elif action == 'decrease':
                    item.quantity = max(1, item.quantity - 1)
                elif action == 'remove':
                    item.delete()
                else:
                    item.quantity = int(action)
                item.save()
                messages.success(request, 'Carrito actualizado.')
            except CartItem.DoesNotExist:
                messages.error(request, 'Error al actualizar el carrito.')
        return redirect('view_cart')
    return render(request, 'orders/cart.html', {'cart': cart})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart, product=product)

    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('view_cart')


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    if item.cart.user == request.user:
        item.delete()
    return redirect('view_cart')


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/my_orders.html', {'orders': orders})


@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status == 'pending':
        order.status = 'cancelled'
        order.save()
        messages.success(request, 'Order cancelled successfully.')
    else:
        messages.error(request, 'This order cannot be cancelled.')
    return redirect('my_orders')


@login_required
def checkout(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        messages.error(request, "No tienes productos en tu carrito.")
        return redirect('view_cart')

    if request.method == 'POST':
        if not cart.items.exists():
            messages.error(request, "Tu carrito está vacío.")
            return redirect('view_cart')

        # Crear la orden
        order = Order.objects.create(
            user=request.user,
            status='pending',
            expiration_date=timezone.now() + timedelta(hours=24)
        )

        # Transferir items del carrito a la orden
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )

        # Limpiar el carrito
        cart.items.all().delete()

        messages.success(
            request, "Tu orden ha sido creada. Por favor, completa el pago en las próximas 24 horas.")
        return redirect('order_confirmation', order_id=order.id)

    return render(request, 'orders/checkout.html', {'cart': cart})


@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_confirmation.html', {'order': order})
