from django.urls import path, include
from core.views.essentials import EssentialView, SingleUrlEssentialView

urlpatterns = [
    path('single/<str:ess_name>', SingleUrlEssentialView.as_view(), name='Covishield'),
    path('states/<str:ess_name>', EssentialView.as_view(), name='essentialUrlList')
]