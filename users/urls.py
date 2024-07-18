from django.urls import path
from .views import SignUpView, admin_dashboard, seller_dashboard, customer_dashboard


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('admin-dashboard/', admin_dashboard, name='admin-dashboard'),
    path('seller-dashboard/', seller_dashboard, name='seller-dashboard'),
    path('customer-dashboard/', customer_dashboard, name='customer-dashboard'),
]
