from djongo.models.fields import ObjectIdField
from rest_framework import serializers
from core.models.community import CommunityPost

#'''
class CommunityPostSerializer(serializers.ModelSerializer):
    #id = ObjectIdField(source='id')
    #_id = ObjectIdField()
    class Meta:
        model = CommunityPost
        #fields = ["name", "phone", "area", "details", "item", "type", "date", "person_id"]
        fields = '__all__'
#'''
#class CommunityPostSerializer(serializers.Serializer):
    