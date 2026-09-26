from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .chat_service import ChatService

class ChatAPIView(APIView):
    def post(self, request):
        user_message = request.data.get('message')
        history = request.data.get('history', [])
        
        if not user_message:
            return Response({'error': 'El mensaje es requerido.'}, status=status.HTTP_400_BAD_REQUEST)
        
        chat_service = ChatService()
        bot_reply = chat_service.get_response(user_message, history)
        
        return Response({'reply': bot_reply}, status=status.HTTP_200_OK)
