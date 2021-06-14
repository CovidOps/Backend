from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response

class VersionView(APIView):
    def get(self, request, *args, **kwargs):
        data = {"version":"0.0.1"}
        return Response(data)