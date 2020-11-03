from rest_framework import serializers


class SpeechRecognizeSerializer(serializers.Serializer):
    audio = serializers.FileField()
    language_code = serializers.CharField(default='en-US')
