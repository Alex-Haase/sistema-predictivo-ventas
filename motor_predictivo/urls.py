"""
URL configuration for motor_predictivo project.
"""
from django.contrib import admin
from django.urls import path, include  # <-- Aquí le agregamos el ', include'

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Esta es la línea mágica que conecta el proyecto principal con tu app:
    path('', include('estimador.urls')),
]