import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'soporte_project.settings')
django.setup()
from tickets.models import Ticket
tickets_data = [
    {
        'titulo': 'Impresora no funciona en sala 201',
        'descripcion': 'La impresora HP LaserJet del laboratorio 201 no imprime. Muestra error de conexión en la pantalla.',
        'prioridad': 'Alta',
        'estado': 'Abierto',
    },
    {
        'titulo': 'Computador lento en recepción',
        'descripcion': 'El computador de recepción tarda más de 5 minutos en iniciar y las aplicaciones se congelan frecuentemente.',
        'prioridad': 'Media',
        'estado': 'En Proceso',
    },
    {
        'titulo': 'Proyector sin señal en auditorio',
        'descripcion': 'El proyector del auditorio principal no detecta señal HDMI desde ningún portátil.',
        'prioridad': 'Alta',
        'estado': 'Abierto',
    },
    {
        'titulo': 'Correo institucional no carga',
        'descripcion': 'Varios usuarios reportan que el correo institucional muestra error 503 al intentar acceder desde el navegador.',
        'prioridad': 'Alta',
        'estado': 'En Proceso',
    },
    {
        'titulo': 'Mouse dañado en oficina 305',
        'descripcion': 'El mouse inalámbrico de la oficina 305 no responde. Se cambiaron las baterías sin éxito.',
        'prioridad': 'Baja',
        'estado': 'Resuelto',
    },
    {
        'titulo': 'Red Wi-Fi intermitente en piso 2',
        'descripcion': 'La conexión Wi-Fi en todo el segundo piso se cae cada 10-15 minutos y tarda en reconectarse.',
        'prioridad': 'Alta',
        'estado': 'Abierto',
    },
    {
        'titulo': 'Software de contabilidad desactualizado',
        'descripcion': 'El software ContaPlus necesita actualización urgente. La versión actual presenta errores al generar reportes mensuales.',
        'prioridad': 'Media',
        'estado': 'Resuelto',
    },
    {
        'titulo': 'Pantalla parpadea en puesto 12',
        'descripcion': 'El monitor del puesto 12 en la sala de sistemas parpadea constantemente, afectando el trabajo del usuario.',
        'prioridad': 'Media',
        'estado': 'Abierto',
    },
]
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