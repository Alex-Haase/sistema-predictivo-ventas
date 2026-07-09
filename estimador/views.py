from .models import HistorialPrediccion
from django.shortcuts import render
from django.http import JsonResponse
import joblib
import os
import numpy as np

# Ruta exacta del modelo
RUTA_MODELO = os.path.join(os.path.dirname(__file__), 'modelo_gradient_boosting.pkl')

# Cargar el modelo al iniciar el servidor
try:
    modelo = joblib.load(RUTA_MODELO)
    print("¡Modelo Gradient Boosting cargado exitosamente en Django!")
except Exception as e:
    modelo = None
    print(f"Error al cargar el modelo: {e}")

def predecir_ventas(request):
    if request.method == 'POST':
        try:
            # 1. Capturar las variables numéricas directas del formulario (Limpias y con respaldo 0)
            latitud = float(request.POST.get('latitud', 0) or 0)
            longitud = float(request.POST.get('longitud', 0) or 0)
            distancia_plaza = float(request.POST.get('distancia_plaza_metros', 0) or 0)
            superficie = float(request.POST.get('superficie_m2', 0) or 0)
            flujo_personas = float(request.POST.get('flujo_personas_diario', 0) or 0)
            competencia = float(request.POST.get('competencia_directa', 0) or 0)
            distancia_metro = float(request.POST.get('distancia_metro_metros', 0) or 0)
            estacionamientos = float(request.POST.get('estacionamientos', 0) or 0)
            poblacion = float(request.POST.get('poblacion_radio_1km', 0) or 0)
            ingreso = float(request.POST.get('ingreso_promedio_hogar', 0) or 0)
            marketing = float(request.POST.get('marketing_mensual', 0) or 0)
            trabajadores = float(request.POST.get('trabajadores', 0) or 0)

            # 2. Capturar las variables categóricas de los selectores
            comuna = request.POST.get('comuna', '')
            tipo_negocio = request.POST.get('tipo_negocio', '')
            zona = request.POST.get('zona', '')

            # 3. Lógica One-Hot Encoding para Comunas
            c_la_florida = 1.0 if comuna == 'La Florida' else 0.0
            c_la_pintana = 1.0 if comuna == 'La Pintana' else 0.0
            c_pirque = 1.0 if comuna == 'Pirque' else 0.0

            # 4. Lógica One-Hot Encoding para Tipo de Negocio
            t_restaurante = 1.0 if tipo_negocio == 'Restaurante' else 0.0
            t_retail = 1.0 if tipo_negocio == 'Retail' else 0.0
            t_servicios = 1.0 if tipo_negocio == 'Servicios' else 0.0
            t_tecnologia = 1.0 if tipo_negocio == 'Tecnologia' else 0.0

            # 5. Lógica One-Hot Encoding para Zona
            z_baja = 1.0 if zona == 'Baja' else 0.0
            z_media = 1.0 if zona == 'Media' else 0.0

            # 6. Construir el array en el ORDEN EXACTO requerido por el modelo (21 características)
            datos_entrada = np.array([[
                latitud, longitud, distancia_plaza, superficie, flujo_personas, 
                competencia, distancia_metro, estacionamientos, poblacion, ingreso, 
                marketing, trabajadores, 
                c_la_florida, c_la_pintana, c_pirque, 
                t_restaurante, t_retail, t_servicios, t_tecnologia, 
                z_baja, z_media
            ]])

            # 7. Realizar la predicción
            if modelo is not None:
                prediccion = modelo.predict(datos_entrada)[0]
                
                # --- GUARDADO AUTOMÁTICO EN ORACLE 11g XE (Reutilizando variables limpias) ---
                try:
                    historial = HistorialPrediccion(
                        latitud=latitud,
                        longitud=longitud,
                        distancia_plaza_metros=distancia_plaza,
                        superficie_m2=superficie,
                        flujo_personas_diario=int(flujo_personas),
                        competencia_directa=int(competencia),
                        distancia_metro_metros=distancia_metro,
                        estacionamientos=int(estacionamientos),
                        poblacion_radio_1km=int(poblacion),
                        ingreso_promedio_hogar=int(ingreso),
                        marketing_mensual=int(marketing),
                        trabajadores=int(trabajadores),
                        comuna=comuna,
                        tipo_negocio=tipo_negocio,
                        zona=zona,
                        ventas_estimadas=float(prediccion)
                    )
                    historial.save() # Ejecuta el INSERT INTO en Oracle
                except Exception as db_err:
                    print(f"Error al guardar en Oracle: {db_err}")
                # -----------------------------------------------------------------------------

                return JsonResponse({'ventas_estimadas': round(float(prediccion), 2)})
            else:
                return JsonResponse({'error': 'El modelo no está disponible en el servidor.'}, status=500)

        except Exception as err:
            return JsonResponse({'error': str(err)}, status=400)

    return render(request, 'estimador/formulario.html')