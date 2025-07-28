from django.shortcuts import render
from .models import Obstaculo
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Obstaculo as ObstaculoModel
from .models import Ubicacion
from .models import EventoSupervision

# Create your views here.

def simulador_vista(request):
    from .models import RutaSimple
    obstaculos_qs = Obstaculo.objects.all()
    obstaculos = [
        {
            'nombre': o.nombre,
            'tipo': o.tipo,
            'latitud': float(o.latitud),
            'longitud': float(o.longitud),
            'descripcion': o.descripcion or ''
        }
        for o in obstaculos_qs
    ]
    # Obtener las rutas 01 Ida y 01 Regreso
    ruta01_ida = RutaSimple.objects.filter(nombre='Ruta 01 Ida').first()
    coords_ruta01_ida = ruta01_ida.coordenadas if ruta01_ida else []
    ruta01_regreso = RutaSimple.objects.filter(nombre='Ruta 01 Regreso').first()
    coords_ruta01_regreso = ruta01_regreso.coordenadas if ruta01_regreso else []
    ruta22_ida = RutaSimple.objects.filter(nombre='Ruta 22 Ida').first()
    coords_ruta22_ida = ruta22_ida.coordenadas if ruta22_ida else []
    ruta22_regreso = RutaSimple.objects.filter(nombre='Ruta 22 Regreso').first()
    coords_ruta22_regreso = ruta22_regreso.coordenadas if ruta22_regreso else []
    ruta44_inicio = RutaSimple.objects.filter(nombre='Ruta 44 Inicio').first()
    coords_ruta44_inicio = ruta44_inicio.coordenadas if ruta44_inicio else []
    ruta44_regreso = RutaSimple.objects.filter(nombre='Ruta 44 Regreso').first()
    coords_ruta44_regreso = ruta44_regreso.coordenadas if ruta44_regreso else []
    contexto = {
        'obstaculos': obstaculos,
        'coords_ruta01': coords_ruta01_ida,
        'coords_ruta01_regreso': coords_ruta01_regreso,
        'coords_ruta22_ida': coords_ruta22_ida,
        'coords_ruta22_regreso': coords_ruta22_regreso,
        'coords_ruta44_inicio': coords_ruta44_inicio,
        'coords_ruta44_regreso': coords_ruta44_regreso,
    }
    return render(request, 'detection_simulator/simulador.html', contexto)

@csrf_exempt
def reportar_obstaculo(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            tipo = data.get('tipo')
            descripcion = data.get('descripcion', '')
            latitud = data.get('latitud')
            longitud = data.get('longitud')
            # Nombre genérico
            nombre = f"Reporte {tipo}"
            from .models import Obstaculo
            Obstaculo.objects.create(
                nombre=nombre,
                tipo=tipo,
                latitud=latitud,
                longitud=longitud,
                descripcion=descripcion
            )
            return JsonResponse({'ok': True})
        except Exception as e:
            return JsonResponse({'ok': False, 'error': str(e)})
    return JsonResponse({'ok': False, 'error': 'Método no permitido'})

@csrf_exempt
@api_view(['GET', 'POST'])
def obstaculo_api(request):
    if request.method == 'GET':
        obstaculos = ObstaculoModel.objects.all()
        data = [
            {
                'id': o.id,
                'nombre': o.nombre,
                'tipo': o.tipo,
                'latitud': float(o.latitud),
                'longitud': float(o.longitud),
                'descripcion': o.descripcion or ''
            }
            for o in obstaculos
        ]
        return Response(data)
    elif request.method == 'POST':
        try:
            data = request.data
            tipo = data.get('tipo')
            descripcion = data.get('descripcion', '')
            latitud = data.get('latitud')
            longitud = data.get('longitud')
            nombre = data.get('nombre', f"Reporte {tipo}")
            obstaculo = ObstaculoModel.objects.create(
                nombre=nombre,
                tipo=tipo,
                latitud=latitud,
                longitud=longitud,
                descripcion=descripcion
            )
            return Response({'ok': True, 'id': obstaculo.id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'ok': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def ubicacion_api(request):
    if request.method == 'GET':
        ubicaciones = Ubicacion.objects.all().order_by('-timestamp')
        data = [
            {
                'id': u.id,
                'usuario': u.usuario,
                'latitud': float(u.latitud),
                'longitud': float(u.longitud),
                'timestamp': u.timestamp.isoformat()
            }
            for u in ubicaciones
        ]
        return Response(data)
    elif request.method == 'POST':
        try:
            data = request.data
            usuario = data.get('usuario', 'anonimo')
            latitud = data.get('latitud')
            longitud = data.get('longitud')
            ubicacion = Ubicacion.objects.create(
                usuario=usuario,
                latitud=latitud,
                longitud=longitud
            )
            return Response({'ok': True, 'id': ubicacion.id}, status=201)
        except Exception as e:
            return Response({'ok': False, 'error': str(e)}, status=400)

@api_view(['GET', 'POST'])
def evento_supervision_api(request):
    if request.method == 'GET':
        eventos = EventoSupervision.objects.all().order_by('-timestamp')
        data = [
            {
                'id': e.id,
                'agente': e.agente,
                'evento': e.evento,
                'timestamp': e.timestamp.isoformat()
            }
            for e in eventos
        ]
        return Response(data)
    elif request.method == 'POST':
        try:
            data = request.data
            agente = data.get('agente', 'desconocido')
            evento = data.get('evento', '')
            ev = EventoSupervision.objects.create(
                agente=agente,
                evento=evento
            )
            return Response({'ok': True, 'id': ev.id}, status=201)
        except Exception as e:
            return Response({'ok': False, 'error': str(e)}, status=400)
