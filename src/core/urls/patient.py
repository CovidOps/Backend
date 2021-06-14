from django.urls import path, include
from core.views.patient import PatientCheckView, PatientSignUpView, PatientUpdateView

urlpatterns = [
    path('<str:phone>/exists', PatientCheckView.as_view(), name='communityPostCreate'),
    path('sign-up', PatientSignUpView.as_view(), name='communityPostGet'),
    path('<str:patient_id>', PatientUpdateView.as_view(), name='communityPostDelete')
]