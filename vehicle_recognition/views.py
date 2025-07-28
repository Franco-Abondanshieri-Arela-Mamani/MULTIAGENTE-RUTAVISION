from django.shortcuts import render

def reconocimiento_formulario(request):
    return render(request, 'vehicle_recognition/reconocimiento_formulario.html')
