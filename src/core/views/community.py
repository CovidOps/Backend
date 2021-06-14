from django.shortcuts import render
from django.http import JsonResponse

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from bson import ObjectId

from core.serializers.community import CommunityPostSerializer
from core.models.community import CommunityPost

class CommunityPostCreateView(APIView):
    def post(self, request, type, *args, **kwargs):
        #console.log(request.data)
        coordinates = request.data['coordinates']
        postdata = request.data
        postdata["type"] = type
        postdata['location'] = {'coordinates':coordinates}
        serializer = CommunityPostSerializer(data=postdata)
        if serializer.is_valid():
            serializer.save()
            resp = {
                'code': 200,
                'message':'Community Post Successfully Added'
            }
            return Response(resp)
        
        resp = {
            'code': 500,
            'error': 'Some error occured'
        }
        
        return Response(resp, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CommunityPostGetView(APIView):
    def post(self, request, type, *args, **kwargs):
        coordinates = request.data["coordinates"]
        qs = CommunityPost.objects.mongo_find(
            {
                'location':{
                    '$geoWithin':{
                        '$centerSphere' : [coordinates, 200.0/6378]
                    }
                },
                'type':type
            }
        )

        # Converting OrderedDict to Dict
        posts = [dict(post) for post in qs]

        # Converting _id and location to pythonic types
        for x in posts:
            x["_id"] = str(x["_id"])
            x["post_id"] = x["_id"]
            x["location"] = dict(x["location"])["coordinates"]
            x["coordinates"] = x["location"]
        
        resp = {
            "code":200,
            "message":"Fetched data successfully",
            "posts": posts
        }
        return Response(resp)

class CommunityPostDeleteView(APIView):
    def delete(self, request, post_id, *args, **kwargs):
        res = CommunityPost.objects.filter(_id=ObjectId(post_id)).delete()
        resp = {
            'code':200,
            'message':'Deleted post successfully'
        }
        return Response(resp)