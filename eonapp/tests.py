import os
import cv2
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D

# Suppress TensorFlow logging and OpenCL usage
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
cv2.ocl.setUseOpenCL(False)

# Initialize the emotion recognition model
model = Sequential()

# Model architecture
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48, 48, 1)))
model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(1024, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(7, activation='softmax'))

# Load pre-trained weights
model_path = r'C:\Users\hilus\PycharmProjects\eon\eonapp\static\model.h5'
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found at: {model_path}")
model.load_weights(model_path)

# Emotion dictionary
emotion_dict = {
    0: "Angry",
    1: "Disgusted",
    2: "Fearful",
    3: "Happy",
    4: "Neutral",
    5: "Sad",
    6: "Surprised"
}

# Haar cascade file path
haar_cascade_path = r'C:\Users\hilus\PycharmProjects\eon\eonapp\static\haarcascade_frontalface_default.xml'
if not os.path.exists(haar_cascade_path):
    raise FileNotFoundError(f"Haar Cascade XML file not found at: {haar_cascade_path}")
face_cascade = cv2.CascadeClassifier(haar_cascade_path)

# Input image path
image_path = r"C:\Users\hilus\PycharmProjects\eon\eonapp\static\smiling-man-outdoors-in-the-city.webp"
frame = cv2.imread(image_path)
if frame is None:
    raise FileNotFoundError(f"Image not found or could not be loaded at: {image_path}")

# Convert image to grayscale
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Detect faces
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

# Process each face
for (x, y, w, h) in faces:
    # Draw rectangle around the face
    cv2.rectangle(frame, (x, y - 50), (x + w, y + h + 10), (255, 0, 0), 2)

    # Crop and preprocess the face region
    roi_gray = gray[y:y + h, x:x + w]
    cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)

    # Predict emotion
    prediction = model.predict(cropped_img)
    maxindex = int(np.argmax(prediction))
    res_emo = emotion_dict[maxindex]

    # Display the detected emotion
    print(f"Detected Emotion: {res_emo}")



