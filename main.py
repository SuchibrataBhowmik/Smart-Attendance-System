from argparse import ArgumentParser
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Notebook
import os
import cv2
import numpy as np
import pandas as pd
import pickle
import csv
import time
import shutil

def DeleteData(btn):
    print("Delete button press !!!")
    # Please write the code for delete a student.
    # Update database
    pass
def recognise():
    dic_file = open("data.pkl", "rb")
    labelName = pickle.load(dic_file)
    if len(labelName)==1:
        master=Tk()
        master.geometry("+400+300")
        master.overrideredirect(1)
        Label(master, text="No student register ...",font=("Verdana", 30), fg='red').pack()
        master.update_idletasks()
        time.sleep(1.5)
        master.destroy()
        return
    exec(open('Recognizer.py').read())
def studentList():
    for widget in studentFrame.winfo_children():
        widget.destroy()
    with (open("data.pkl", "rb")) as openfile:
        while True:
            try:
                students=(pickle.load(openfile))
            except EOFError:
                break
    if len(students)==1:
        master=Tk()
        master.geometry("+400+300")
        master.overrideredirect(1)
        Label(master, text="No student register ...",font=("Verdana", 30), fg='red').pack()
        master.update_idletasks()
        time.sleep(1.5)
        master.destroy()
        return
    
    tablayout=Notebook(studentFrame)
    tab1=Frame(tablayout)
    tab1.pack(fill="both")

    for row in range(len(students)):
        for column in range(3):
            if row==0:
                if column==0:
                    label = Label(tab1, text="ID", bg="white", fg="black", padx=3, pady=3)
                    label.config(font=('Arial', 14))
                    label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                    tab1.grid_columnconfigure(column, weight=1)
                if column==1:
                    label = Label(tab1, text="NAME", bg="white", fg="black", padx=3, pady=3)
                    label.config(font=('Arial', 14))
                    label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                    tab1.grid_columnconfigure(column, weight=1)
                if column==2:
                    label = Label(tab1, text="REMOVE", bg="white", fg="black", padx=3, pady=3)
                    label.config(font=('Arial', 14))
                    label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                    tab1.grid_columnconfigure(column, weight=1)
            else:
                if column==2:
                    button=Button(tab1,text="Delete",bg="blue",fg="white",padx=3,pady=3)
                    button.grid(row=row,column=column,sticky="nsew",padx=1,pady=1)
                    # Delete button does not work.
                    # If you want to delete the student. Then write DeleteData function
                    button['command']=lambda btn=button:DeleteData(btn) 
                    tab1.grid_columnconfigure(column,weight=1)
                if column==1:
                    label=Label(tab1,text=students[row],bg="black",fg="white", font=('Arial', 14), padx=3,pady=3)
                    label.grid(row=row,column=column,sticky="nsew",padx=1,pady=1)
                    tab1.grid_columnconfigure(column,weight=1)
                if column==0:
                    label=Label(tab1,text=row,bg="black",fg="white",padx=3,pady=3)
                    label.grid(row=row,column=column,sticky="nsew",padx=1,pady=1)
                    tab1.grid_columnconfigure(column,weight=1)
    tablayout.add(tab1,text="Student List")
    tablayout.pack(fill="both")
    Button(studentFrame, text='Present Sheet', font=("Verdana", 20), bg='green', command=lambda:exec(open('show.py').read())).pack()
    Button(studentFrame, text='BACK', font=("Verdana", 20), bg='yellow', command=lambda:raise_frame(mainFrame)).pack()   
    raise_frame(studentFrame)
def takeFace():
    name=nameField.get()
    if name=='':
        return
        
    parent_dir='label faces/'        #Create new folder for load new student's face
    subdir=os.listdir(parent_dir)
    directory=len(subdir)+1
    path = os.path.join(parent_dir,str( directory)) 
    os.mkdir(path)   

    exec(open('captureFace.py').read())

    dic_file = open("data.pkl", "rb")       #Load new student name and his ID in Dictionary
    labelName = pickle.load(dic_file)
    labelName.update({directory:name})
    pickle.dump(labelName, open("data.pkl", "wb"))

    with open('present.csv','a',newline='') as csvfile:     #Add row for new student
        csvwriter=csv.writer(csvfile)
        csvwriter.writerow([nameField.get()])

    print(labelName)
def train():
    name=nameField.get()
    if name=='':
        return
    exec(open('Trainer.py').read())
    raise_frame(submitFrame)
def raise_frame(frame):
    frame.tkraise()
def exitFrame():
    window.destroy()

def argparser():
    parser = ArgumentParser(description="Initialise the system")
    parser.add_argument('-i', '--initialise', default=False, help="Is initialise the system?(True/False) Destroy all data.")
    return parser.parse_args()

if __name__ == '__main__':
    args = argparser()
    initialise = args.initialise
    if initialise:
        labelName={0:'ZERO'} # For Dictionary Initialise
        dic_file = open("data.pkl", "wb")
        pickle.dump(labelName, dic_file)
        dic_file.close()
        print("Dictionary Initialise !!!")
        with open('present.csv','w',newline='') as csvfile:   # For present sheet Initialise
            csvwriter=csv.writer(csvfile)
            csvwriter.writerow(['Name'])
        print("CSV file Initialise !!!")
        for subdir in os.listdir('label faces'): shutil.rmtree(os.path.join('label faces', subdir))
        if os.path.isfile('trainingData.yml'):os.remove('trainingData.yml')
        print('All faces deleted !!!')


    window = Tk()
    window.geometry("500x500")
    window.title("Smart Attendence System")

    mainFrame= Frame(window)
    registerFrame = Frame(window)
    submitFrame = Frame(window)
    studentFrame = Frame(window)
    for frame in (mainFrame, registerFrame, submitFrame, studentFrame):
        frame.grid(row=0, column=0, sticky='news')
    
    Label(mainFrame, text='Home Page',font=("Verdana", 20), fg='blue').pack(pady=30)
    Button(mainFrame, text='REGISTER',font=("Verdana", 20), bg='blue', command=lambda:raise_frame(registerFrame)).pack()
    Button(mainFrame, text='ATTENDANCE', font=("Verdana", 20), bg='green', command=recognise).pack()
    Button(mainFrame, text='STUDENT LIST', font=("Verdana", 20), bg='orange', command=studentList).pack()
    Button(mainFrame, text='EXIT', font=("Verdana", 20), bg='red', command=exitFrame).pack()

    Label(registerFrame, text='REGISTER',font=("Verdana", 20)).pack()
    Label(registerFrame, text='*Please enter name', fg='red').place(x=250,y=100)
    Label(registerFrame, text='Name : ').pack(side=LEFT,padx=10)
    nameField = Entry(registerFrame, font=("Verdana", 20))
    nameField.pack(side=RIGHT,padx=10)
    Button(registerFrame, text='CAPTURE', font=("Verdana", 20),bg='green', command=takeFace).place(x=150,y=180)
    Button(registerFrame, text='BACK', font=("Verdana", 20), bg='yellow', command=lambda:raise_frame(mainFrame)).place(x=80,y=240)
    Button(registerFrame, text='SUBMIT', font=("Verdana", 20),bg='red', command=train).place(x=200,y=240)

    Label(submitFrame, text='Submission Successful').pack()
    Label(submitFrame, text='.........................').pack()
    Button(submitFrame, text='Go to Home Page', font=("Verdana", 20), command=lambda:raise_frame(mainFrame)).pack()

    raise_frame(mainFrame)

    window.mainloop()


