from django.db import migrations
from django.utils import timezone


def set_updated_at(apps, schema_editor):
    CartItem = apps.get_model('orders', 'CartItem')
    for item in CartItem.objects.all():
        if not item.updated_at:
            item.updated_at = item.created_at or timezone.now()
            item.save()


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_alter_cartitem_updated_at'),
    ]

    operations = [
        migrations.RunPython(set_updated_at),
    ]
