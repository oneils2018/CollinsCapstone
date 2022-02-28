import numpy as np
import math as math
import os
import tensorflow as tf
import cv2
from keras.preprocessing import image

#Load trained model
loaded_model = tf.keras.models.load_model('tensorflow_model.h5')

def image_classifier(index,index3):
    img = image.load_img(str(index3)+"zoom"+str(index)+".png", target_size=(480, 640))
    result=loaded_model.predict(np.expand_dims(img,axis=0))
    result = np.round_(result,decimals=2)
    cube_prediction=result[0][1]
    cone_prediction=result[0][0]
    prediction = ""
    if(cube_prediction > cone_prediction):
        prediction = "Predicted object: Cube"
    else:
        prediction = "Predicted object: Cone"
    return prediction
