from django.urls import path
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ChatMessage
from .serializers import ChatMessageSerializer, ChatQuerySerializer
from .services import get_ai_assistant_response

class AIChatAPIView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = ChatQuerySerializer(data=request.data)
        if serializer.is_valid():
            msg = serializer.validated_data['message']
            reply = get_ai_assistant_response(request.user, msg)
            return Response({
                'user_message': msg,
                'assistant_reply': reply
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AIChatHistoryAPIView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response([])
        msgs = ChatMessage.objects.filter(user=request.user).order_by('timestamp')
        return Response(ChatMessageSerializer(msgs, many=True).data)

urlpatterns = [
    path('chat/', AIChatAPIView.as_view(), name='api_ai_chat'),
    path('history/', AIChatHistoryAPIView.as_view(), name='api_ai_history'),
]
