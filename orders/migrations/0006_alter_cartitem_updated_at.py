# Generated by Django 4.2.13 on 2024-07-23 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_set_expiration_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='updated_at',
            field=models.DateTimeField(),
        ),
    ]