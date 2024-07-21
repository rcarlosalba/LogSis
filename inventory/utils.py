from django.utils import timezone
from datetime import timedelta


def is_order_expired(order):
    """
    comprueba si han pasado más de 24 horas desde que se creó el pedido
    """
    return timezone.now() - order.created > timedelta(hours=24)


def release_product(order):
    """
    liberar el producto al inventario si el pedido ha expirado
    """
    if is_order_expired(order) and order.status == 'PENDING':
        order.product.quantity += order.quantity
        order.product.save()
        order.status('CANCELLED')
        return True
    return False
