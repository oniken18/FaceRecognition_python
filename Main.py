import os
import pickle

import cv2

import AddPic

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
cascPath = THIS_FOLDER + r"\venv\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
recognizer = cv2.face.LBPHFaceRecognizer_create()

if os.path.exists('trainer.yml'):
    recognizer.read('trainer.yml')

isOpen = False
roi_gray = []
labels = {}
if os.path.exists('labels.pickle'):
    with open("labels.pickle", 'rb') as f:
        og_labels = pickle.load(f)
    labels = {v: k for k, v in og_labels.items()}

cap = cv2.VideoCapture(0)
while True:

    ret, frame = cap.read()
    cv2.putText(frame, 'Q = Quit', (10, 20), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (0, 255, 0), 1)
    cv2.putText(frame, 'C = Capture', (10, 50), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (0, 255, 0), 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
    color = (225, 0, 0)
    for (x, y, w, h) in faces:

        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y - 50:y + h + 20, x - 20:x + w + 20]

        if os.path.exists('trainer.yml'):
            id_, conf = recognizer.predict(roi_gray)
            if 45 <= conf <= 85 and id_ < 2:
                cv2.putText(frame, labels[id_], (x, y - 55), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1)

        cv2.rectangle(frame, (x - 20, y - 50), (x + 20 + w, y + 20 + h), color, 2)

    cv2.imshow('frame', frame)

    if cv2.waitKey(20) & 0xff == ord('q'):
        if len(roi_gray) < 0:
            img_item = "my-Image.jpg"
            cv2.imwrite(img_item, roi_gray)

        break

    if cv2.waitKey(20) & 0xff == ord('c'):
        if not isOpen:
            isOpen = True
            capture_item = "capture-Image.jpg"
            cv2.imwrite(capture_item, roi_color)
            AddPic.start()
            isOpen = False

            recognizer.read('trainer.yml')

            with open("labels.pickle", 'rb') as f:
                og_labels = pickle.load(f)
                labels = {v: k for k, v in og_labels.items()}

cap.release()
cv2.destroyAllWindows()
