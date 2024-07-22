from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView
from .forms import CustomUserCreationForm, CustomLoginForm, CustomPasswordResetForm
from .decorators import user_type_required


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.",
                               extra_tags='bg-red-500 text-white')
        else:
            messages.error(request, "Invalid username or password.",
                           extra_tags='bg-red-500 text-white')
    else:
        form = CustomLoginForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('login')


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'registration/password_reset_form.html'
    success_url = reverse_lazy('password_reset_done')
    email_template_name = 'registration/password_reset_email.html'
    html_email_template_name = 'registration/password_reset_email_html.html'
    subject_template_name = 'registration/password_reset_subject.txt'


@login_required
def dashboard_view(request):
    user_type = request.user.user_type
    if user_type in ['owner', 'admin']:
        return render(request, 'dashboard/admin_dashboard.html')
    elif user_type == 'seller':
        return render(request, 'dashboard/seller_dashboard.html')
    else:  # customer
        return render(request, 'dashboard/customer_dashboard.html')


@user_type_required('owner', 'admin')
def admin_dashboard(request):
    return render(request, 'dashboard/admin_dashboard.html')


@user_type_required('owner', 'seller', 'admin')
def seller_dashboard(request):
    return render(request, 'dashboard/seller_dashboard.html')


@user_type_required('customer')
def customer_dashboard(request):
    return render(request, 'dashboard/customer_dashboard.html')
