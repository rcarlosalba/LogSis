from django.db import migrations
from django.utils import timezone
from datetime import timedelta


def set_expiration_date(apps, schema_editor):
    Order = apps.get_model('orders', 'Order')
    for order in Order.objects.all():
        if order.expiration_date == order.created_at:  # Si la fecha de expiración es igual a la fecha de creación
            order.expiration_date = order.created_at + timedelta(hours=24)
            order.save()


class Migration(migrations.Migration):

    dependencies = [
        # Reemplaza XXXX con el número de la migración anterior
        ('orders', '0004_order_expiration_date_alter_orderitem_price'),
    ]

    operations = [
        migrations.RunPython(set_expiration_date),
    ]
