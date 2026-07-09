from django.urls import path
from . import views

urlpatterns = [
    # Esto le dice a Django: "Cuando alguien entre a la página principal, ejecuta la vista predecir_ventas"
    path('', views.predecir_ventas, name='predecir_ventas'),
]