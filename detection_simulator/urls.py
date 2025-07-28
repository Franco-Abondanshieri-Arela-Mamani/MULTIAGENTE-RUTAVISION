from django.urls import path
from . import views

urlpatterns = [
    path('simulador/', views.simulador_vista, name='simulador'),
    path('reportar_obstaculo/', views.reportar_obstaculo, name='reportar_obstaculo'),
    path('api/obstaculos/', views.obstaculo_api, name='obstaculo_api'),
    path('ubicacion_api/', views.ubicacion_api, name='ubicacion_api'),
    path('evento_supervision_api/', views.evento_supervision_api, name='evento_supervision_api'),
] 