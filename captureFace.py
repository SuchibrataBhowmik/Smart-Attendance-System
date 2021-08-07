import cv2
import os
from tkinter import *

def raise_frame(frame):
    frame.tkraise()
def face_extractor(img):
    face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray,1.3,5)
    if faces is():
        return None
    for(x,y,w,h) in faces:
        cropped_face = img[y:y+h, x:x+w]
    return cropped_face

cap = cv2.VideoCapture(0)
count = 0
parent_dir='label faces/'
subdir=os.listdir(parent_dir)
directory=len(subdir)
path=os.path.join(parent_dir,str(directory))

while True:
    ret, frame = cap.read()
    if not ret:
        print('camera not found')
        break
    if face_extractor(frame) is not None:
        count+=1
        face = cv2.resize(face_extractor(frame),(200,200))
        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

        file_name_path = path+'/user'+str(count)+'.jpg'
        cv2.imwrite(file_name_path,face)

        window="face viewer"
        cv2.namedWindow(window) 
        cv2.moveWindow(window, 500,0)
        cv2.putText(face,str(count),(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
        cv2.imshow(window,face)
    else:
        print("face not found !!!")

    cv2.waitKey(1)
    if count==100: break
cap.release()
cv2.destroyAllWindows()
print('Colleting Samples Complete!!!')


