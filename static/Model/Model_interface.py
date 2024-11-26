# import tensorflow as tf
# from tensorflow.keras import layers, models
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import LabelEncoder
# from tensorflow.keras.models import load_model
# import pandas as pd
# import cv2
# import numpy as np
# import os

# def load():
#     return load_model('static/Model/Labelling_model.keras')

# import pickle

# def load_label_encoders():
#     with open('static/Model/label_encoders/gender_encoder.pkl', 'rb') as f:
#         le_gender = pickle.load(f)
#     with open('static/Model/label_encoders/clothing_type_encoder.pkl', 'rb') as f:
#         le_clothing_type = pickle.load(f)
#     with open('static/Model/label_encoders/color_encoder.pkl', 'rb') as f:
#         le_color = pickle.load(f)
#     with open('static/Model/label_encoders/occassion_encoder.pkl', 'rb') as f:
#         le_occassiom = pickle.load(f)

#     gender_labels = le_gender.classes_
#     clothing_type_labels = le_clothing_type.classes_
#     color_labels = le_color.classes_
#     occassion_labels = le_occassiom.classes_
#     return gender_labels, clothing_type_labels, color_labels, occassion_labels



# def predict(image):

#     print("the image is",image)
#     target_size = (112, 112)
#     # Process a new image for prediction
#     image_path="media/user_images/"+image.name
#     print("the image path is",image_path)
#     new_image = cv2.imread(image_path)
#     new_image = cv2.resize(new_image, target_size)  # Resize to match training images
#     new_image = np.expand_dims(new_image, axis=0) / 255.0

#     # Make predictions
#     predictions = load().predict(new_image)

#     gender_labels, clothing_type_labels, color_labels, occassiom_labels=load_label_encoders()
#     # Extract predictions
#     gender_prediction = predictions[0]
#     clothing_type_prediction = predictions[1]
#     color_prediction = predictions[2]
#     occassion_prediction=predictions[3]

#     le_gender = LabelEncoder().fit(gender_labels)
#     le_clothing_type = LabelEncoder().fit(clothing_type_labels)
#     le_color = LabelEncoder().fit(color_labels)
#     le_occassiom = LabelEncoder().fit(occassiom_labels)

    
    
#     # Decode predictions to get the corresponding labels
#     predicted_gender_label = le_gender.inverse_transform([int(round(gender_prediction[0][0]))])[0]
#     predicted_clothing_type_label = le_clothing_type.inverse_transform([np.argmax(clothing_type_prediction[0])])[0]
#     predicted_color_label = le_color.inverse_transform([np.argmax(color_prediction[0])])[0]
#     predicted_occassion_label=le_occassiom.inverse_transform([np.argmax(occassion_prediction[0])])[0]


#     return predicted_gender_label,predicted_clothing_type_label,predicted_color_label,predicted_occassion_label

import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import load_model
import pandas as pd
import cv2
import numpy as np
import os
import pickle

def load():
    return load_model('static/Model/Labelling_model.keras')

def load_label_encoders():
    with open('static/Model/label_encoders/gender_encoder.pkl', 'rb') as f:
        le_gender = pickle.load(f)
    with open('static/Model/label_encoders/clothing_type_encoder.pkl', 'rb') as f:
        le_clothing_type = pickle.load(f)
    with open('static/Model/label_encoders/color_encoder.pkl', 'rb') as f:
        le_color = pickle.load(f)
    with open('static/Model/label_encoders/occassion_encoder.pkl', 'rb') as f:
        le_occassiom = pickle.load(f)

    gender_labels = le_gender.classes_
    clothing_type_labels = le_clothing_type.classes_
    color_labels = le_color.classes_
    occassion_labels = le_occassiom.classes_
    return gender_labels, clothing_type_labels, color_labels, occassion_labels

def predict(image):
    print("the image is", image)
    target_size = (112, 112)
    # Process a new image for prediction
    image_path = "media/" + image.name
    print("the image path is", image_path)
    new_image = cv2.imread(image_path)
    new_image = cv2.resize(new_image, target_size)  # Resize to match training images
    new_image = np.expand_dims(new_image, axis=0) / 255.0

    # Make predictions
    predictions = load().predict(new_image)

    # Load label encoders and their labels
    gender_labels, clothing_type_labels, color_labels, occassion_labels = load_label_encoders()
    
    # Extract predictions
    gender_prediction = predictions[0]
    clothing_type_prediction = predictions[1]
    color_prediction = predictions[2]
    occassion_prediction = predictions[3]

    # Decode predictions to get the corresponding labels
    predicted_gender_label = gender_labels[np.round(gender_prediction[0][0]).astype(int)]
    predicted_clothing_type_label = clothing_type_labels[np.argmax(clothing_type_prediction[0])]
    predicted_color_label = color_labels[np.argmax(color_prediction[0])]
    predicted_occassion_label = occassion_labels[np.argmax(occassion_prediction[0])]

    return predicted_clothing_type_label, predicted_color_label, predicted_occassion_label
