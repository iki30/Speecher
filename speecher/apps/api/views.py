import speech_recognition as sr

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from speecher.apps.api.serializers import SpeechRecognizeSerializer


class SpeechRecognizeView(viewsets.GenericViewSet):
    serializer_class = SpeechRecognizeSerializer

    @action(detail=False, methods=['post'])
    def recognize(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        transcript = self.get_transcript_by_audio(
            serializer.validated_data['audio'], serializer.validated_data['language_code']
        )

        return Response({
            'data': [
                (item['transcript'], self._round_to_two(item.get('confidence')))
                for item in transcript['alternative']
            ]}
        )

    def get_transcript_by_audio(self, audio, language):
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio) as source:
            audio = recognizer.record(source)
        try:
            audio_output = recognizer.recognize_google(
                audio, language=language, show_all=True
            )
        except sr.RequestError:
            return Response({
                "error": {"error_message": "API was unreachable or unresponsive"}
            })
        except sr.UnknownValueError:
            return Response({
                "error": {"error_code": 1, "error_message": "Recognition service return unexpected error"}
            })
        return audio_output

    def _round_to_two(self, confidence):
        return confidence and round(confidence, 2)
