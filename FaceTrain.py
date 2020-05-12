import os
import pickle

import cv2
import numpy as np
from PIL import Image

def start():
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    filterFoldersDir = os.path.join(THIS_FOLDER, 'recognizerFilter')

    currId = 0
    label_Ids = {}
    x_train = []
    y_label = []
    cascPath = r"C:\Users\eitan\PycharmProjects\FaceRecognition\venv\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascPath)

    recognizer = cv2.face.LBPHFaceRecognizer_create()

    for root, dirs, files in os.walk(filterFoldersDir):
        for file in files:
            if file.endswith("JPG") or file.endswith("jpg") or file.endswith("png"):
                path = os.path.join(root, file)
                label = os.path.basename(os.path.dirname(path))

                print(label)
                if not label in label_Ids:
                    label_Ids[label] = currId
                    currId += 1

                id_ = label_Ids[label]

                pil_image = Image.open(path).convert("L")
                imageArray = np.array(pil_image, 'uint8')

                faces = faceCascade.detectMultiScale(imageArray, scaleFactor=1.3, minNeighbors=5)

                for (x, y, w, h) in faces:
                    roi = imageArray[y:y + h, x:x + w]

                    x_train.append(roi)
                    y_label.append(id_)

    with open("labels.pickle", 'wb') as f:
        pickle.dump(label_Ids, f)

    if len(y_label) > 0:
        recognizer.train(x_train, np.array(y_label))
        recognizer.save("trainer.yml")
    else:
        print('no Faces Found!')
