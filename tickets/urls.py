from django.urls import path
from . import views
from . import chat_views
app_name = 'tickets'
urlpatterns = [
    path('', views.lista_tickets, name='lista_tickets'),
    path('<int:ticket_id>/', views.detalle_ticket, name='detalle_ticket'),
    path('estado/<str:estado>/', views.filtrar_por_estado, name='filtrar_por_estado'),
    path('<int:ticket_id>/cambiar-estado/', views.cambiar_estado, name='cambiar_estado'),
    path('api/chat/', chat_views.ChatAPIView.as_view(), name='api_chat'),
]