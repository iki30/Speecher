from rest_framework import serializers

from speecher.apps.recources import LANGUAGES_CODE


class SpeechRecognizeSerializer(serializers.Serializer):
    audio = serializers.FileField()
    language_code = serializers.ChoiceField(choices=LANGUAGES_CODE, default='en-US')

