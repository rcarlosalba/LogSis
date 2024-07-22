from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (SignUpView, admin_dashboard, seller_dashboard, customer_dashboard,
                    login_view, logout_view, CustomPasswordResetView, dashboard_view)


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('admin-dashboard/', admin_dashboard, name='admin-dashboard'),
    path('seller-dashboard/', seller_dashboard, name='seller-dashboard'),
    path('customer-dashboard/', customer_dashboard, name='customer-dashboard'),

    # Cambio de contraseña
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='registration/password_change_form.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='registration/password_change_done.html'), name='password_change_done'),

    # Restablecimiento de contraseña
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'), name='password_reset_complete'),

    # Dashboard
    path('dashboard/', dashboard_view, name='dashboard'),
]
