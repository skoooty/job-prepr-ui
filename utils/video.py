import cv2
import numpy as np
from PIL import Image
from multiprocessing.resource_sharer import stop

def find_face(image):
    try:
        image1 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')

        faces = face_cascade.detectMultiScale(
                                                image1,
                                                scaleFactor=1.3,
                                                minNeighbors=3,
                                                minSize=(30, 30)
                                                        )
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            just_face = image[y:y + h, x:x + w]
            just_face=np.array(Image.fromarray(just_face)
            )
            return just_face
    except:
        return None
