# inventory/views.py

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Product
from .forms import ProductForm
from orders.models import Cart, CartItem


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.user_type in ['owner', 'admin', 'seller']

    def handle_no_permission(self):
        return redirect('inventory:home')


class HomeView(ListView):
    model = Product
    template_name = 'inventory/home.html'
    context_object_name = 'products'
    paginate_by = 12  # Número de productos por página

    def get_queryset(self):
        return Product.objects.all().order_by('-id')


class ProductListView(ListView):
    model = Product
    template_name = 'inventory/product_list.html'
    context_object_name = 'products'
    paginate_by = 12  # Número de productos por página

    def get_queryset(self):
        return Product.objects.order_by('-created_at')


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'inventory/product_detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        return super().get_queryset().select_related('created_by', 'last_modified_by')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object

        # Obtener productos relacionados basados en la misma categoría
        related_products = Product.objects.filter(
            Q(category=product.category) & ~Q(id=product.id)
        ).distinct()[:5]  # Limitamos a 5 productos relacionados

        context['related_products'] = related_products
        return context

    def post(self, request, *args, **kwargs):
        if request.user.user_type != 'customer':
            messages.error(
                request, "Solo los clientes pueden agregar productos al carrito.")
            return redirect(request.path)

        product = self.get_object()
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart, product=product)

        if not item_created:
            cart_item.quantity += 1
            cart_item.save()

        messages.success(
            request, f"{product.name} ha sido agregado a tu carrito.")
        return redirect('inventory:product_detail', pk=product.pk)


class ProductCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'inventory/product_form.html'
    success_url = reverse_lazy('inventory:product_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.last_modified_by = self.request.user
        if form.cleaned_data.get('imagen'):
            form.instance.imagen_url = ''  # Limpiar la URL si se sube una imagen
        elif form.cleaned_data.get('imagen_url'):
            form.instance.imagen = None  # Limpiar la imagen si se proporciona una URL
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'inventory/product_form.html'
    success_url = reverse_lazy('inventory:product_list')

    def form_valid(self, form):
        form.instance.last_modified_by = self.request.user
        if form.cleaned_data.get('imagen'):
            form.instance.imagen_url = ''  # Limpiar la URL si se sube una imagen
        elif form.cleaned_data.get('imagen_url'):
            form.instance.imagen = None  # Limpiar la imagen si se proporciona una URL
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Product
    template_name = 'inventory/product_confirm_delete.html'
    success_url = reverse_lazy('inventory:product_list')
