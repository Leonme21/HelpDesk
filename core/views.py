from django.shortcuts import render
from tickets.models import Ticket
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