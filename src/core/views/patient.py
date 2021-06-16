from django.shortcuts import render
from django.http import JsonResponse

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from bson import ObjectId

from core.serializers.patient import Patient, PatientSerializer
from core.models.patient import Patient

class PatientCheckView(APIView):
    def get(self, request, phone, *args, **kwargs):
        qs = Patient.objects.mongo_find({'phone' : phone})
        if qs.count() == 0:
            resp = {
                "code": 201,
                "message": "Patient does not exist.",
                "id" : None,
                "name" : None,
                "area" : None,
                "address" : None,
                "location": None
            }
            return Response(resp)

        for patient in qs:
            resp = {
                "code": 200,
                "message": "Patient exists.",
                "id" : str(patient["_id"]),
                "name" : patient["name"],
                "area" : patient["area"],
                "address" : patient["address"],
                "location": patient["location"]["coordinates"]
            }
        return Response(resp)

class PatientSignUpView(APIView):
    def post(self, request, *args, **kwargs):
        coordinates = request.data['coordinates']
        patientData = request.data
        patientData['location'] = {'coordinates':coordinates}
        serializer = PatientSerializer(data=patientData)
        if serializer.is_valid():
            serializer.save()
            resp = {
                'code': 200,
                'message':'Signed up successfully',
                'id': serializer.data["_id"]
            }
            return Response(resp)
        
        resp = {
            'code': 500,
            'error': 'Some error occured'
        }
        
        return Response(resp, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PatientUpdateView(APIView):
    def patch(self, request, patient_id, *args, **kwargs):
        updatedData = request.data
        '''
        for patient in Patient.objects.filter(_id=ObjectId(patient_id)):
            patient["area"] = updatedData["area"]
            patient["address"] = updatedData["address"]
            patient["location"]["coordinates"] = updatedData["coordinates"]
            patient.save()
        '''
        nLocation = {"type":"Point", "coordinates":updatedData["coordinates"]}
        Patient.objects.filter(_id=ObjectId(patient_id)).update(
            area=updatedData["area"], 
            address=updatedData["address"], 
            location=nLocation
        )
        resp = {
            'code':200,
            'message':"Updated details successfully"
        }
        return Response(resp)