from django.db import models
class Ticket(models.Model):
    PRIORIDAD_CHOICES = [
        ('Baja', 'Baja'),
        ('Media', 'Media'),
        ('Alta', 'Alta'),
    ]
    ESTADO_CHOICES = [
        ('Abierto', 'Abierto'),
        ('En Proceso', 'En Proceso'),
        ('Resuelto', 'Resuelto'),
    ]
    titulo = models.CharField(max_length=200, verbose_name='Título')
    descripcion = models.TextField(verbose_name='Descripción')
    prioridad = models.CharField(
        max_length=10,
        choices=PRIORIDAD_CHOICES,
        default='Media',
        verbose_name='Prioridad',
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='Abierto',
        verbose_name='Estado',
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación',
    )
    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'
    def __str__(self):
        return f'#{self.pk} — {self.titulo}'