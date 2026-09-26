# HelpDesk — Sistema de Soporte Técnico con IA

Este es un sistema de gestión de tickets de soporte técnico desarrollado en Django. El proyecto cuenta con una base de datos local SQLite para el control de tickets, consumo de un microservicio externo para el directorio de agentes, y un **asistente inteligente integrado** (Chatbot) usando Google Gemini y Django Rest Framework (DRF).

---

## 📂 Arquitectura y Estructura de Archivos

### 1. `core/` (Aplicación de vistas generales)
Maneja las páginas de información general y el consumo de APIs de terceros.
- **`views.py`**: Contiene las funciones para renderizar la página de inicio (con el resumen de los tickets), la página "Acerca de", y la vista del directorio de agentes (la cual consume los datos mediante `requests` a un microservicio en Render).
- **`urls.py`**: Define las rutas `/`, `/acerca/` y `/agentes/`.

### 2. `tickets/` (Aplicación de negocio y Chatbot)
Aquí vive toda la lógica de los tickets y de la Inteligencia Artificial.
- **`models.py`**: Define la entidad principal `Ticket` en la base de datos, con campos como título, descripción, prioridad (Baja, Media, Alta) y estado (Abierto, En Proceso, Resuelto).
- **`views.py`**: Funciones clásicas de Django para listar tickets, filtrarlos por estado, ver detalles y cambiar sus estados.
- **`chat_service.py` (Cerebro IA)**: Contiene la clase `ChatService`. Es el motor de la inteligencia artificial. Lee la base de datos local de Tickets y el microservicio de Agentes, construye un contexto dinámico y se comunica con Google Gemini usando la librería oficial.
- **`chat_views.py` (Proxy IA)**: Expone un endpoint `POST /api/chat/` usando DRF. Recibe los mensajes del frontend y los pasa a `chat_service.py`. Esto evita que la API Key se exponga en el navegador.

### 3. `soporte_project/` (Configuración global)
- **`settings.py`**: Configuraciones de Django. Aquí se conectan las apps, se configura la BD SQLite, y se carga el archivo `.env`.
- **`urls.py`**: Enrutador principal que despacha hacia `core/` y `tickets/`.

### 4. `templates/` (Frontend HTML/CSS/JS)
- **`base.html`**: La plantilla maestra. Tiene el diseño CSS principal, la barra de navegación y **el código HTML, CSS y JS del widget del Chatbot**. Todas las demás páginas "heredan" y se insertan dentro de esta plantilla.
- **`core/` y `tickets/`**: Contienen las vistas específicas (tablas, formularios, dashboard).

### 5. Archivos en Raíz
- **`.env`**: Archivo seguro (ignorado por Git) que guarda tus variables de entorno, específicamente tu `GEMINI_API_KEY`.
- **`db.sqlite3`**: Base de datos ligera de Django.
- **`manage.py`**: El script principal para correr comandos de Django (como `runserver` o `makemigrations`).
- **`requirements.txt`**: Lista de todas las dependencias instaladas (Django, requests, google-genai, djangorestframework, etc.).

---

## 🔄 Flujo Completo: Desde el Click hasta las Entidades

Para entender cómo funciona el proyecto de inicio a fin, imaginemos que un usuario entra a la página web y le pregunta al Chatbot: *"¿Me pueden ayudar con mi ticket de mi computadora rota?"*

### Paso 1: El Frontend (Interacción del usuario)
El usuario está en el navegador. La vista web está construida gracias al archivo `base.html`. Al escribir su pregunta y darle a "Enviar":
1. El **JavaScript** incrustado en `base.html` captura el texto.
2. Agrega una animación de "Escribiendo..." (tres puntos rebotando).
3. Envía el texto (junto con los últimos mensajes del historial) usando un `fetch` (petición HTTP POST) hacia tu servidor en la ruta secreta: `/tickets/api/chat/`.

### Paso 2: El Backend / Proxy de DRF (Recepción de la petición)
La petición llega al servidor Django y es interceptada por `chat_views.py`.
1. Este archivo funciona como un escudo de seguridad (Proxy).
2. Valida que haya un mensaje y llama a nuestro motor lógico: el `ChatService`.

### Paso 3: Las Entidades y el Contexto (Construyendo el cerebro)
Dentro de `chat_service.py` se ejecuta la magia antes de hablar con Google:
1. **Entidades Locales:** Ejecuta un query a la base de datos de Django: `Ticket.objects.filter(estado='Abierto')`. Extrae los IDs, títulos y descripciones.
2. **Entidades Externas:** Hace un `requests.get` al microservicio en Render para traer a todos los agentes especialistas en línea.
3. El servicio junta todo eso en un **System Prompt** invisible para el usuario que le dice a la IA: *"Eres un asistente, este es el HelpDesk. Aquí tienes los tickets abiertos reales y estos son los agentes disponibles. Ahora responde al usuario."*

### Paso 4: Inteligencia Artificial (Llamada al LLM)
Con el contexto armado y el mensaje del usuario, `chat_service.py` envía la solicitud a Google Gemini:
1. Intenta conectarse al modelo rápido (`gemini-3.5-flash-lite`).
2. Si los servidores de Google se saturan (Error 503), nuestro código espera unos segundos e intenta nuevamente (Exponential Backoff).
3. Si falla 3 veces seguidas, cambia automáticamente al modelo más grande y pesado de respaldo (`gemma-4-31b`).

### Paso 5: Respuesta al Frontend
1. Google devuelve la respuesta generada por la IA (ej. *"Claro, tu ticket sobre la computadora rota tiene prioridad Alta y está abierto. El especialista Carlos te ayudará pronto."*).
2. `chat_views.py` empaqueta esta respuesta en formato JSON.
3. El **JavaScript** en el navegador recibe el JSON, esconde los tres puntitos de "Escribiendo..." y renderiza la burbuja con el texto del bot en la pantalla del usuario.

¡Todo esto ocurre en cuestión de milisegundos y con un diseño de arquitectura modular y segura!
