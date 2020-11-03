from rest_framework.routers import SimpleRouter

from .views import SpeechRecognizeView

app_name = 'api'

router = SimpleRouter()

router.register('', SpeechRecognizeView, 'speech_recognize')


urlpatterns = (
    router.urls
)