from rest_framework import serializers
from .models import ChatMessage

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'role', 'message', 'timestamp']

class ChatQuerySerializer(serializers.Serializer):
    message = serializers.CharField(required=True)
