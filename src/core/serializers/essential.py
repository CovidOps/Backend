from rest_framework import serializers
from core.models.essential import Essential, State, SingleUrlEssential

class StateSerializer(serializers.Serializer):
    state = serializers.CharField()
    url = serializers.CharField()


class EssentialSerializer(serializers.ModelSerializer):
    urls = StateSerializer(many=True, read_only=True)
    class Meta:
        model = Essential
        fields = '__all__'

class SingleUrlEssentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = SingleUrlEssential
        fields = '__all__'