import os
from numpy.random import rand
from cv2 import VideoCapture
from tensorflow import expand_dims
from tensorflow.keras.metrics import categorical_crossentropy
from tensorflow.io import read_file
from tensorflow.image import decode_jpeg,resize,flip_left_right
from tensorflow.keras.utils import image_dataset_from_directory
from keras.models import Model,Sequential,load_model
from keras.layers import Input,Conv2D,MaxPooling2D,Dropout,Flatten,Dense,GlobalAveragePooling2D,BatchNormalization
from dotenv import load_dotenv
load_dotenv()
from logger_local.Logger import Logger
from gender_detection import GenderClassifier

model=GenderClassifier()
model.train()
