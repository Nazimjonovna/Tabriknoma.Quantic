from django.urls import path
from .views import  TextView, WishesView, ListenVoiceView


urlpatterns = [
    # path('text/', TextView.as_view(), name='text-to-voice'),
    path('wish-list/', WishesView.as_view()),
    path('wish-create/', TextView.as_view()),
    path('wish-listen/', ListenVoiceView.as_view()),
]


