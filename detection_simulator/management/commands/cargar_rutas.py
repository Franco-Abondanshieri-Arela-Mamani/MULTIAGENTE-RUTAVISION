import os
import json
from django.core.management.base import BaseCommand
from detection_simulator.models import Ruta, PuntoRuta
from django.conf import settings

RUTAS = [
    { 'archivo': 'ruta01Inicio.json', 'nombre': 'Ruta 01 Ida', 'color': '#FF0000' },
    { 'archivo': 'ruta01Regreso.json', 'nombre': 'Ruta 01 Regreso', 'color': '#FF0000' },
    { 'archivo': 'ruta22Inicio.json', 'nombre': 'Ruta 22 Ida', 'color': '#0000FF' },
    { 'archivo': 'ruta22Regreso.json', 'nombre': 'Ruta 22 Regreso', 'color': '#0000FF' },
    { 'archivo': 'ruta44Inicio.json', 'nombre': 'Ruta 44 Ida', 'color': '#800080' },
    { 'archivo': 'ruta44Regreso.json', 'nombre': 'Ruta 44 Regreso', 'color': '#800080' },
]

class Command(BaseCommand):
    help = 'Carga las rutas desde archivos JSON en json_rutas/ a la base de datos.'

    def handle(self, *args, **kwargs):
        base_dir = os.path.join(settings.BASE_DIR, 'json_rutas')
        for ruta_info in RUTAS:
            archivo = os.path.join(base_dir, ruta_info['archivo'])
            if not os.path.exists(archivo):
                self.stdout.write(self.style.WARNING(f'No se encontró {archivo}'))
                continue
            with open(archivo, encoding='utf-8') as f:
                data = json.load(f)
            locations = data.get('trip', {}).get('locations', [])
            if not locations:
                self.stdout.write(self.style.WARNING(f'No hay puntos en {archivo}'))
                continue
            ruta, created = Ruta.objects.get_or_create(nombre=ruta_info['nombre'], defaults={'color': ruta_info['color']})
            if not created:
                ruta.puntos.all().delete()  # Limpia puntos previos
            for i, punto in enumerate(locations):
                PuntoRuta.objects.create(
                    ruta=ruta,
                    orden=i,
                    latitud=punto['lat'],
                    longitud=punto['lon']
                )
            self.stdout.write(self.style.SUCCESS(f'Ruta {ruta.nombre} cargada con {len(locations)} puntos.')) 