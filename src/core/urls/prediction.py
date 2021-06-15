from django.urls import path, include
from core.views.audio import AudioView
from core.views.image import ImageView

urlpatterns = [
    path('audio', AudioView.as_view(), name='audio'),
    path('image', ImageView.as_view(), name='image')
]