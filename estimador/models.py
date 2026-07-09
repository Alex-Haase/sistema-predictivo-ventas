from django.db import models

class HistorialPrediccion(models.Model):
    # Campos numéricos del formulario
    latitud = models.FloatField()
    longitud = models.FloatField()
    distancia_plaza_metros = models.FloatField()
    superficie_m2 = models.FloatField()
    flujo_personas_diario = models.IntegerField()
    competencia_directa = models.IntegerField()
    distancia_metro_metros = models.FloatField()
    estacionamientos = models.IntegerField()
    poblacion_radio_1km = models.IntegerField()
    ingreso_promedio_hogar = models.IntegerField()
    marketing_mensual = models.IntegerField()
    trabajadores = models.IntegerField()
    
    # Campos de texto (Selectores)
    comuna = models.CharField(max_length=100)
    tipo_negocio = models.CharField(max_length=100)
    zona = models.CharField(max_length=50)
    
    # El resultado que escupe la IA y cuándo se calculó
    ventas_estimadas = models.FloatField()
    fecha_consulta = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Predicción {self.id} - {self.comuna} (${self.ventas_estimadas})"