from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.conf import settings

import os
import sys

from rest_framework.views import APIView
from rest_framework.response import Response

from core.apps import CoreConfig
import pandas as pd
import numpy as np
import librosa

#Features to be extracted
features =  [
                'chroma_stft', 'rmse', 'spectral_centroid', 'spectral_bandwidth', 'rolloff', 'zero_crossing_rate',
                'mfcc1', 'mfcc2', 'mfcc3', 'mfcc4', 'mfcc5', 'mfcc6', 'mfcc7', 'mfcc8', 'mfcc9', 'mfcc10', 
                'mfcc11', 'mfcc12', 'mfcc13', 'mfcc14', 'mfcc15', 'mfcc16', 'mfcc17', 'mfcc18', 'mfcc19', 'mfcc20'
            ]

ALLOWED_EXTENSIONS_AUDIO = {'wav', 'mp3'}
def allowed_file_audio(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_AUDIO

# Model and I/O details
scaler = CoreConfig.scaler
interAud = CoreConfig.interAud
input_details_aud = CoreConfig.input_details_aud
output_details_aud = CoreConfig.output_details_aud

def preprocessAUDIO(fn_wav):
    y, sr = librosa.load(fn_wav, mono=True, duration=3)
    chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
    rmse = librosa.feature.rms(y=y)
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    zcr = librosa.feature.zero_crossing_rate(y)
    mfcc = librosa.feature.mfcc(y=y, sr=sr)

    feature_row = {        
        'chroma_stft': np.mean(chroma_stft),
        'rmse': np.mean(rmse),
        'spectral_centroid': np.mean(spectral_centroid),
        'spectral_bandwidth': np.mean(spectral_bandwidth),
        'rolloff': np.mean(rolloff),
        'zero_crossing_rate': np.mean(zcr),        
    }
    for i, c in enumerate(mfcc):
        feature_row[f'mfcc{i+1}'] = np.mean(c)

    df = pd.DataFrame(columns = features)
    df = df.append(feature_row, ignore_index = True)
    X_test = scaler.transform(df)
    
    return X_test

class AudioView(APIView):
    def post(self, request, *args, **kwargs):
        data = {}

        if 'file' not in request.FILES:
            data["prediction"] = "No file found"
            data["status"] = 300
            print(data, file=sys.stderr)
            return Response(data)
        
        f = request.FILES["file"]
        
        if not allowed_file_audio(f.name):
            data["prediction"] = "File extension is invalid"
            data["status"] = 400
            print(data, file=sys.stderr)
            return Response(data)
        
        fname = default_storage.save(f.name, f)
        fpath = settings.MEDIA_ROOT + os.path.sep + fname

        try:
            listed = preprocessAUDIO(fpath)
            input_data = np.array(listed, dtype=np.float32)
            interAud.set_tensor(input_details_aud[0]['index'], input_data)
            interAud.invoke()
            output_data = interAud.get_tensor(output_details_aud[0]['index'])
            # predicted = classes[int(np.round(output_data[0][0]))]
            # print(output_data[0][0], file=sys.stderr)
            
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