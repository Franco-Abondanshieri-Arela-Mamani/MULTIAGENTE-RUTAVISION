from django.urls import path
from .views import reconocimiento_formulario

urlpatterns = [
    path('formulario/', reconocimiento_formulario, name='formulario_reconocimiento'),
] 