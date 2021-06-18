from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from core.serializers.essential import EssentialSerializer, SingleUrlEssentialSerializer
from core.models.essential import Essential, SingleUrlEssential

class EssentialView(APIView):
    def get(self, request, ess_name, *args, **kwargs):
        try:
            qs = Essential.objects.get(name=ess_name)
            serializer = EssentialSerializer(qs)
            resp = {
                'code':200,
                'message':'Fetched state URLs',
                'urls': serializer.data["urls"]
            }
        except:
            resp = {
                'code':500,
                'message':'No url found',
                'urls':None
            }
        return Response(resp)

class SingleUrlEssentialView(APIView):
    def get(self, request, ess_name, *args, **kwargs):
        try:
            qs = SingleUrlEssential.objects.get(name=ess_name)
            serializer = SingleUrlEssentialSerializer(qs)
            resp = {
                'code':200,
                'message':'Fetched single URLs',
                'url':serializer.data["url"]
            }
        except:
            resp = {
                'code':500,
                'message':'No url found',
                'url':None
            }
        return Response(resp)