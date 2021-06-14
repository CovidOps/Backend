from django.urls import path, include
from core.views.community import CommunityPostCreateView, CommunityPostGetView, CommunityPostDeleteView

urlpatterns = [
    path('<int:type>', CommunityPostCreateView.as_view(), name='communityPostCreate'),
    path('<int:type>/nearby', CommunityPostGetView.as_view(), name='communityPostGet'),
    path('<str:post_id>', CommunityPostDeleteView.as_view(), name='communityPostDelete')
]