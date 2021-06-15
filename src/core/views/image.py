import os
import sys
from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response

# Prediction-oriented imports
from core.apps import CoreConfig
import matplotlib.pyplot as plt
import cv2
import numpy as np

# Extension check
ALLOWED_EXTENSIONS_IMAGE = {'png', 'jpg', 'jpeg'}
def allowed_file_image(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_IMAGE

# Preprocessing function
def preprocessIMG(path):
    image1 = plt.imread(path)
    image1 = cv2.resize(image1, (224, 224))
    image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
    images = []
    images.append(image1)
    #images = np.array(images) / 255.0
    return images

# Model and I/O details
interImg = CoreConfig.interImg
input_details_img = CoreConfig.input_details_img
output_details_img = CoreConfig.output_details_img
#classes  = CoreConfig.classes

class ImageView(APIView):
    def post(self, request, *args, **kwargs):
        data = {}

        if 'file' not in request.FILES:
            data["prediction"] = "No file found"
            data["status"] = 300
            print(data, file=sys.stderr)
            return Response(data)
        
        f = request.FILES["file"]
        
        if not allowed_file_image(f.name):
            data["prediction"] = "File extension is invalid"
            data["status"] = 400
            print(data, file=sys.stderr)
            return Response(data)
        
        fname = default_storage.save(f.name, f)
        fpath = settings.MEDIA_ROOT + os.path.sep + fname
        
        try:
            listed = preprocessIMG(fpath)
            input_data = np.array(listed, dtype=np.float32) / 255.0
            interImg.set_tensor(input_details_img[0]['index'], input_data)
            interImg.invoke()
            output_data = interImg.get_tensor(output_details_img[0]['index'])
            #predicted = classes[int(np.round(output_data[0][0]))]
            #print(output_data[0][0], predicted, file=sys.stderr)
            
            data["prediction"] = str(output_data[0][0])
            data["status"] = 200
            if default_storage.exists(fpath):
                default_storage.delete(fpath)
            return Response(data)
        except:
            if default_storage.exists(fpath):
                default_storage.delete(fpath)
            data["prediction"] = "Some error occured"
            data["status"] = 500
            return Response(data)