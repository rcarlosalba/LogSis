# inventory/views.py

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Product
from .forms import ProductForm


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.user_type in ['owner', 'admin', 'seller']

    def handle_no_permission(self):
        return redirect('inventory:home')


class HomeView(ListView):
    model = Product
    template_name = 'inventory/home.html'
    context_object_name = 'products'


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'inventory/product_list.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'inventory/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'inventory/product_form.html'
    success_url = reverse_lazy('inventory:product_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.last_modified_by = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'inventory/product_form.html'
    success_url = reverse_lazy('inventory:product_list')

    def form_valid(self, form):
        form.instance.last_modified_by = self.request.user
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Product
    template_name = 'inventory/product_confirm_delete.html'
    success_url = reverse_lazy('inventory:product_list')
