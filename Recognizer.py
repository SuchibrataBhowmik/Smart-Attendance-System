import cv2
import pickle
import pandas as pd
import time
    
def attendence(label,full_time):
    f=pd.read_csv("present.csv")
    f[full_time][label-1]='Y'
    f.to_csv('present.csv', index=False)

t= time.localtime()
full_time=time.strftime("%H:%M:%S", t)
f=pd.read_csv("present.csv")
f[full_time]='N'
f.to_csv('present.csv', index=False)

dic_file = open("data.pkl", "rb")
labelName = pickle.load(dic_file)
print(labelName)

face_recognizer=cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read('trainingData.yml')

cap = cv2.VideoCapture(0)
frm_no = 0
while 1:
    ret, img = cap.read()
    if not ret:
        print('camera not found')
        break
    face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray,1.3,5)
    if faces is():
        cv2.putText(img,'Face Not Found',(20,50),cv2.FONT_HERSHEY_DUPLEX,1,(0,0,255),1)
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        roi_gray=cv2.resize(roi_gray,(200,200))
        #cv2.imshow('roi_gray',roi_gray)
        label,confidence=face_recognizer.predict(roi_gray)
        print("confidence:",confidence)
        print("label:",label)
        predicted_name=labelName[label]
        if(confidence>50):
            continue
        attendence(label,full_time)
        cv2.putText(img,predicted_name,(x,y),cv2.FONT_HERSHEY_DUPLEX,1,(255,0,0),1)

    cv2.imshow('img',img)
    cv2.waitKey(30)
    frm_no+=1
    if frm_no==30: break

cap.release()
cv2.destroyAllWindows()


