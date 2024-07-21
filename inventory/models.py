# inventory/models.py

from django.db import models
from django.conf import settings
from .constants import PRODUCT_CATEGORIES, ORDER_STATUS
from PIL import Image
import io
from django.core.files.base import ContentFile


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    imagen_url = models.URLField(max_length=500, blank=True, null=True)
    imagen = models.ImageField(upload_to='products/', null=True, blank=True)
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

    def save(self, *args, **kwargs):
        if self.imagen:
            img = Image.open(self.imagen)
            if img.height > 800 or img.width > 800:
                output_size = (800, 800)
                img.thumbnail(output_size)
                img_byte_arr = io.BytesIO()
                img_format = 'JPEG' if self.imagen.name.lower().endswith(
                    ('.jpg', '.jpeg')) else 'PNG'
                img.save(img_byte_arr, format=img_format)
                img_byte_arr = img_byte_arr.getvalue()
                file_name = self.imagen.name
                self.imagen.delete(save=False)
                self.imagen.save(file_name, ContentFile(
                    img_byte_arr), save=False)
        super().save(*args, **kwargs)

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
