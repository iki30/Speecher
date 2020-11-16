from rest_framework import serializers

from speecher.apps.recources import LANGUAGES_CODE


class SpeechRecognizeSerializer(serializers.Serializer):
    audio = serializers.FileField()
    language_code = serializers.ChoiceField(choices=LANGUAGES_CODE, default='en-US')

    def validate_audio(self, file):
        if not file._name.endswith('flac'):
            raise serializers.ValidationError('Файл должен быть расширения flac')

        return file
