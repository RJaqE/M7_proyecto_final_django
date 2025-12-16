from django.contrib import admin
from django.urls import path, include 

urlpatterns = [
    path('admin/', admin.site.urls),
    # Rutas de autenticación estándar (login, logout, password_change, etc.)
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('productos.urls')), 
]