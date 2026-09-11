from django.contrib import admin
from .models import Ticket
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'prioridad', 'estado', 'fecha_creacion')
    list_filter = ('estado', 'prioridad')
    search_fields = ('titulo', 'descripcion')