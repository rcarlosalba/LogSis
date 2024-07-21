from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price',
                  'quantity', 'category', 'sku',
                  'imagen_url', 'imagen']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['imagen'].widget.attrs.update(
            {'class': 'form-control-file'})
        self.fields['imagen_url'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'https://example.com/image.jpg'})

    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen')
        if imagen:
            if not imagen.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                raise forms.ValidationError(
                    'El archivo debe ser una imagen (PNG, JPG, JPEG o GIF).')
            if imagen.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError(
                    'El tamaño de la imagen no debe exceder 5MB.')
        return imagen

    def clean(self):
        cleaned_data = super().clean()
        imagen = cleaned_data.get('imagen')
        imagen_url = cleaned_data.get('imagen_url')
        if imagen and imagen_url:
            raise forms.ValidationError(
                'Por favor, proporcione una imagen o una URL de imagen, no ambas.')
        return cleaned_data
