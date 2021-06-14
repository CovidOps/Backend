from djongo.models.fields import ObjectIdField
from rest_framework import serializers
from core.models.community import CommunityPost

class CommunityPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityPost
        fields = '__all__'
    