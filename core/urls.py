"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from inventory import error_views
from inventory.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    # home view
    path('', HomeView.as_view(), name='home'),
    # users app
    path('users/', include('users.urls')),
    # inventory app
    path('inventory/', include('inventory.urls')),
    # orders app
    path('orders/', include('orders.urls')),
    # browser reload
    path('__reload__/', include('django_browser_reload.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Error views
handler403 = error_views.error_403
handler404 = error_views.error_404
