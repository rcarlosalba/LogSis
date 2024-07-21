# inventory/models.py

from django.db import models
from django.conf import settings
from .constants import PRODUCT_CATEGORIES, ORDER_STATUS


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=20, choices=PRODUCT_CATEGORIES)
    sku = models.CharField(max_length=50, unique=True)  # Stock Keeping Unit
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='products_created'
    )
    last_modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='products_modified'
    )

    def __str__(self):
        return self.name


class RelatedProduct(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='related_products')
    related_to = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('product', 'related_to')

    def __str__(self):
        return f"{self.product.name} - Related to: {self.related_to.name}"
