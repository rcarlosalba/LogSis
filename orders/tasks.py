from django.utils import timezone
from .models import Order


def cancel_expired_orders():
    expired_orders = Order.objects.filter(
        status='pending', expiration_date__lt=timezone.now())
    for order in expired_orders:
        order.status = 'cancelled'
        order.save()
