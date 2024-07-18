from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm
from .decorators import user_type_required

# Create your views here.


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


@user_type_required('owner', 'admin')
def admin_dashboard(request):
    return render(request, 'dashboard/admin_dashboard.html')


@user_type_required('owner', 'seller', 'admin')
def seller_dashboard(request):
    return render(request, 'dashboard/seller_dashboard.html')


@user_type_required('customer')
def customer_dashboard(request):
    return render(request, 'dashboard/customer_dashboard.html')
