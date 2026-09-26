import os
import time
import logging
from google import genai
from google.genai import types
from google.genai.errors import APIError
from tickets.models import Ticket

logger = logging.getLogger(__name__)

class ChatService:
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            logger.error("GEMINI_API_KEY no está configurada")
        self.client = genai.Client(api_key=self.api_key)
        self.primary_model = 'gemini-3.5-flash-lite'
        self.fallback_model = 'gemma-4-31b'
        self.max_retries = 3
        self.backoff_times = [2, 3, 5]

    def _get_dynamic_context(self):
        # Obtener tickets abiertos para inyectarlos en el contexto
        open_tickets = Ticket.objects.filter(estado='Abierto')
        context = "Contexto dinámico de la base de datos de HelpDesk:\n"
        if open_tickets.exists():
            context += "Tickets actualmente abiertos:\n"
            for t in open_tickets:
                context += f"- Ticket #{t.pk}: {t.titulo} (Prioridad: {t.prioridad})\n  Descripción: {t.descripcion}\n"
        else:
            context += "Actualmente no hay tickets abiertos.\n"
            
        # Obtener información del microservicio de agentes
        try:
            import requests
            url_microservicio = "https://microservicio-agentes.onrender.com/api/agentes"
            response = requests.get(url_microservicio, timeout=5)
            if response.status_code == 200:
                agentes = response.json()
                if agentes:
                    context += "\nDirectorio de Agentes de Soporte (Microservicio externo):\n"
                    for agente in agentes:
                        nombre = agente.get('nombre', 'Desconocido')
                        especialidad = agente.get('especialidad', 'General')
                        context += f"- {nombre} (Especialidad: {especialidad})\n"
        except Exception as e:
            logger.error(f"Error al obtener agentes del microservicio para el chatbot: {e}")
            
        return context

    def get_response(self, user_message, history=None):
        if history is None:
            history = []

        system_instruction = (
            "Eres un asistente inteligente para el sistema de HelpDesk.\n"
            "Tu objetivo es ayudar a los usuarios con sus tickets y consultas.\n"
            f"{self._get_dynamic_context()}"
        )

        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            max_output_tokens=4096,
        )
        
        contents = []
        for msg in history:
            role = "user" if msg.get('role') == 'user' else "model"
            contents.append(
                types.Content(role=role, parts=[types.Part.from_text(text=msg.get('text', ''))])
            )
        
        contents.append(
            types.Content(role="user", parts=[types.Part.from_text(text=user_message)])
        )

        # Retry logic with exponential backoff and fallback
        for attempt in range(self.max_retries + 1):
            try:
                # Try primary model
                response = self.client.models.generate_content(
                    model=self.primary_model,
                    contents=contents,
                    config=config
                )
                return response.text
            except APIError as e:
                is_503 = getattr(e, 'code', None) == 503 or "503" in str(e)
                if is_503:
                    if attempt < self.max_retries:
                        sleep_time = self.backoff_times[attempt]
                        logger.warning(f"Error 503 con {self.primary_model}. Reintentando en {sleep_time} segundos (Intento {attempt + 1}/{self.max_retries})...")
                        time.sleep(sleep_time)
                    else:
                        logger.warning(f"Error 503 persistente con {self.primary_model}. Usando modelo de respaldo {self.fallback_model}...")
                        try:
                            # Try fallback model
                            response = self.client.models.generate_content(
                                model=self.fallback_model,
                                contents=contents,
                                config=config
                            )
                            return response.text
                        except Exception as fallback_error:
                            logger.error(f"Error en el modelo de respaldo: {fallback_error}")
                            return "Lo siento, el servicio no está disponible temporalmente por alta demanda."
                else:
                    logger.error(f"APIError inesperado: {e}")
                    return "Ocurrió un error al procesar tu solicitud."
            except Exception as e:
                logger.error(f"Error inesperado en ChatService: {e}")
                return "Ocurrió un error interno al conectar con el asistente."
