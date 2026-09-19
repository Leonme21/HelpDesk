from django.shortcuts import render
from tickets.models import Ticket
import requests

def home(request):
    total = Ticket.objects.all().count()
    abiertos = Ticket.objects.filter(estado='Abierto').count()
    en_proceso = Ticket.objects.filter(estado='En Proceso').count()
    resueltos = Ticket.objects.filter(estado='Resuelto').count()
    context = {
        'total': total,
        'abiertos': abiertos,
        'en_proceso': en_proceso,
        'resueltos': resueltos,
    }
    return render(request, 'core/home.html', context)

def acerca(request):
    return render(request, 'core/acerca.html')

def directorio_agentes(request):
    url_microservicio = "http://127.0.0.1:5000/api/agentes" # URL de prueba local
    
    try:
        response = requests.get(url_microservicio, timeout=5)
        response.raise_for_status() # Verifica si hubo error HTTP
        agentes = response.json()
    except Exception as e:
        agentes = []
        print(f"Error al consumir el microservicio: {e}")
        
    context = {
        'agentes': agentes
    }
    return render(request, 'core/agentes.html', context)