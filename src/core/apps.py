from django.apps import AppConfig
from django.conf import settings
import os
import pickle

# Prediction-oriented imports
from joblib import dump, load
import tensorflow as tf

class CoreConfig(AppConfig):
    name = 'core'
    classes = ['Covid', 'Non-Covid']

    # create path to models
    image_model_path = os.path.join(settings.ML, 'model.tflite')
    audio_model_path = os.path.join(settings.ML, 'model_tflite_tabular_audio.tflite')
    scaler_path = os.path.join(settings.ML, 'std_scaler.bin')
    scaler = load(scaler_path)

    # interAud = tf.lite.Interpreter(model_path="model_tflite_tabular_audio.tflite")
    interAud = tf.lite.Interpreter(model_path=audio_model_path)
    interAud.allocate_tensors()
    input_details_aud = interAud.get_input_details()
    output_details_aud = interAud.get_output_details()
    input_shape_aud = input_details_aud[0]['shape']
    
    # interImg = tf.lite.Interpreter(model_path="model.tflite")
    interImg = tf.lite.Interpreter(model_path=image_model_path)
    interImg.allocate_tensors()
    input_details_img = interImg.get_input_details()
    output_details_img = interImg.get_output_details()
    input_shape_img = input_details_img[0]['shape']