import os
import json
from django.core.management.base import BaseCommand
from detection_simulator.models import RutaSimple
from django.conf import settings

class Command(BaseCommand):
    help = 'Carga una lista de coordenadas desde un archivo JSON en RutaSimple.'

    def add_arguments(self, parser):
        parser.add_argument('archivo', type=str, help='Nombre del archivo JSON en json_rutas1/')
        parser.add_argument('nombre', type=str, help='Nombre de la ruta')
        parser.add_argument('--color', type=str, default='#FF0000', help='Color de la ruta')
        parser.add_argument('--descripcion', type=str, default='', help='Descripción de la ruta')

    def handle(self, *args, **options):
        archivo = os.path.join(settings.BASE_DIR, 'json_rutas1', options['archivo'])
        if not os.path.exists(archivo):
            self.stdout.write(self.style.ERROR(f'No se encontró {archivo}'))
            return
        with open(archivo, encoding='utf-8') as f:
            coords = json.load(f)
        ruta, created = RutaSimple.objects.get_or_create(
            nombre=options['nombre'],
            defaults={
                'color': options['color'],
                'coordenadas': coords,
                'descripcion': options['descripcion']
            }
        )
        if not created:
            ruta.coordenadas = coords
            ruta.color = options['color']
            ruta.descripcion = options['descripcion']
            ruta.save()
        self.stdout.write(self.style.SUCCESS(f"Ruta {options['nombre']} cargada con {len(coords)} coordenadas.")) 