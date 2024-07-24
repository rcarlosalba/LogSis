from django.db import migrations, models


def set_default_prices(apps, schema_editor):
    OrderItem = apps.get_model('orders', 'OrderItem')
    for item in OrderItem.objects.all():
        if item.price == 0:
            item.price = item.product.price
            item.save()


class Migration(migrations.Migration):

    dependencies = [
        # Reemplaza XXXX con el número de la migración anterior
        ('orders', '0002_remove_orderitem_created_at_and_more'),
    ]

    operations = [
        migrations.RunPython(set_default_prices),
        migrations.AlterField(
            model_name='orderitem',
            name='price',
            field=models.DecimalField(max_digits=10, decimal_places=2),
        ),
    ]
