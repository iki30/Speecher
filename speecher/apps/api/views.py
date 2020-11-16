import json

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from speecher.apps.api.serializers import SpeechRecognizeSerializer

from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


class RequestError(Exception):
    pass


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
        data = self.get_audio_to_flac(audio)
        response = self.recognize_google_api(data, language)
        return self.normalize_response_to_json(response)

    def recognize_google_api(self, data, language):
        audio_rate = 48000  # audio sample rate must be between 8 kHz and 48 kHz inclusive

        url = self.generate_speech_api_url(language)
        request = Request(url, data=data, headers={"Content-Type": "audio/x-flac; rate={}".format(audio_rate)})

        try:
            response = urlopen(request, timeout=10000)
        except HTTPError as e:
            raise RequestError("recognition request failed: {}".format(e.reason))
        except URLError as e:
            raise RequestError("recognition connection failed: {}".format(e.reason))
        return response.read().decode("utf-8")

    def get_audio_to_flac(self, audio):
        """
        Метод, который преобразует нашу бинарные данные в flac
        :param audio:
        :return:
        """
        return audio.read()

    def normalize_response_to_json(self, response_text):
        result = None
        for line in response_text.split("\n"):
            temp_result = json.loads(line)["result"]
            if len(temp_result):
                result = temp_result[0]
                break
        return result

    def generate_speech_api_url(self, language, key=None):
        key = key or "AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw"
        url = "http://www.google.com/speech-api/v2/recognize?{}".format(urlencode({
            "client": "chromium",
            "lang": language,
            "key": key,
        }))

        return url

    def _round_to_two(self, confidence):
        return confidence and round(confidence, 2)
