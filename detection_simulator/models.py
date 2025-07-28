from django.db import models

# Create your models here.

class Obstaculo(models.Model):
    TIPOS_OBSTACULO = [
        ('bache', 'Bache'),
        ('poste', 'Poste'),
        ('muro', 'Muro'),
        ('vehiculo_mal_estacionado', 'Vehículo Mal Estacionado'),
        ('rampa', 'Rampa Elevada'),
        ('escalera', 'Escalera'),
        ('cruce_peligroso', 'Cruce Peligroso'),
        ('vereda_estrecha', 'Vereda Estrecha'),
        ('zona_trafico_intenso', 'Zona de Tráfico Intenso'),
        ('otro', 'Otro'),
    ]

    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50, choices=TIPOS_OBSTACULO, default='otro')
    latitud = models.DecimalField(max_digits=9, decimal_places=6)
    longitud = models.DecimalField(max_digits=9, decimal_places=6)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} ({self.tipo}) en ({self.latitud}, {self.longitud})"

    class Meta:
        verbose_name = "Obstáculo"
        verbose_name_plural = "Obstáculos"

class RutaSimple(models.Model):
    nombre = models.CharField(max_length=100)
    color = models.CharField(max_length=20, default='#000000')
    coordenadas = models.JSONField()
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Ubicacion(models.Model):
    usuario = models.CharField(max_length=100, default="anonimo")
    latitud = models.DecimalField(max_digits=9, decimal_places=6)
    longitud = models.DecimalField(max_digits=9, decimal_places=6)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} en ({self.latitud}, {self.longitud}) @ {self.timestamp}"

    class Meta:
        verbose_name = "Ubicación"
        verbose_name_plural = "Ubicaciones"

class EventoSupervision(models.Model):
    agente = models.CharField(max_length=100)
    evento = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.agente}: {self.evento} @ {self.timestamp}"

    class Meta:
        verbose_name = "Evento de Supervisión"
        verbose_name_plural = "Eventos de Supervisión"
