import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'soporte_project.settings')
django.setup()
from tickets.models import Ticket
tickets_data = [] # Los datos se cargarán directamente desde la base de datos
created_count = 0
for data in tickets_data:
    ticket, created = Ticket.objects.get_or_create(
        titulo=data['titulo'],
        defaults=data,
    )
    if created:
        created_count += 1
        print(f'  [+] Creado: {ticket}')
    else:
        print(f'  [-] Ya existia: {ticket}')
print(f'\nTotal creados: {created_count} de {len(tickets_data)} tickets.')