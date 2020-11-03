from io import BytesIO
from unittest.mock import patch

from django.test import TestCase

from rest_framework import status


class SpeechRecognizeTests(TestCase):
    def setUp(self):
        pass

    @patch('api.views.SpeechRecognizeView.get_transcript_by_audio')
    def test_transcript(self, get_transcript_by_audio):
        title = 'test transcript'
        get_transcript_by_audio.return_value = {'alternative': [{'transcript': title}]}

        response = self.client.post(
            '/api/recognize/', data={'audio': BytesIO(b'test')}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data'][0], (title, None))

    # Можно через side_effect проверить исключения
