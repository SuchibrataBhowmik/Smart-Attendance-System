import time
import cv2
import os
import numpy as np
import tkinter as tk
import tkinter.ttk as ttk

def fetch_Face_FaceID():
    faces=[]
    faceID=[]
    for path,subdir,filenames in os.walk("label faces"):
        for filename in filenames:     
            id=os.path.basename(path)
            img_path=os.path.join(path,filename)
            #print("img_path:",img_path)
            #print("id:",id) 
            test_img=cv2.imread(img_path)
            gray_img = cv2.cvtColor(test_img,cv2.COLOR_BGR2GRAY)
            faces.append(gray_img)
            faceID.append(int(id))
    return faces,faceID

def training(faces,faceID):
    face_recognizer=cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.train(faces,np.array(faceID))
    return face_recognizer

master=tk.Tk()
master.geometry("+400+300")
master.overrideredirect(1)      #clear window top manager bar

tk.Label(master, text="Loading...",font=("Verdana", 30), fg='red').grid(row=0, column=0)
progress=ttk.Progressbar(master,orient="horizontal",length=500,mode='determinate')
progress.grid(row=1, column=0)

tk.Label(master, text="0% / 100").grid(row=1, column=1)
progress['value']=0
master.update_idletasks()

faces,faceID=fetch_Face_FaceID()
tk.Label(master, text="10% / 100").grid(row=1, column=1)
progress['value']=10
master.update_idletasks()

face_recognizer=training(faces,faceID)
tk.Label(master, text="70% / 100").grid(row=1, column=1)
progress['value']=70
master.update_idletasks()

face_recognizer.write('trainingData.yml')
tk.Label(master, text="100% / 100").grid(row=1, column=1)
progress['value']=100
master.update_idletasks()
time.sleep(2)
master.destroy()

print("Model successfully save")


