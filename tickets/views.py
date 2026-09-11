from django.shortcuts import render, get_object_or_404, redirect
from .models import Ticket
def lista_tickets(request):
    tickets = Ticket.objects.all().order_by('-fecha_creacion')
    context = {'tickets': tickets}
    return render(request, 'tickets/lista_tickets.html', context)
def detalle_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    context = {'ticket': ticket}
    return render(request, 'tickets/detalle_ticket.html', context)
def filtrar_por_estado(request, estado):
    tickets = Ticket.objects.filter(estado__iexact=estado)
    context = {
        'tickets': tickets,
        'estado_filtro': estado,
    }
    return render(request, 'tickets/lista_tickets.html', context)
def cambiar_estado(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    if ticket.estado == 'Abierto':
        ticket.estado = 'En Proceso'
    elif ticket.estado == 'En Proceso':
        ticket.estado = 'Resuelto'
    ticket.save()
    return redirect('tickets:detalle_ticket', ticket_id=ticket.pk)