from django.contrib import admin
from django.urls import path, include
from core.views.version import VersionView
from core.urls import community, patient, version, prediction, essentials

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
    path('version/', include(version)),
    path('community/', include(community)),
    path('patient/', include(patient)),
    path('prediction/', include(prediction)),
    path('essentials/', include(essentials))
]
