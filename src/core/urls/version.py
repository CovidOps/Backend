from django.urls import path, include
from core.views.version import VersionView

urlpatterns = [
    path('', VersionView.as_view(), name='communityPostCreate'),
]