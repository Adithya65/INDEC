import cv2
import imutils
import numpy as np
import argparse
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import serial
import time
import random
from random import *
line=[]
zzz=0
peop=1


ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser.reset_input_buffer()
 
# define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('INDECjson.json', scope)
client = gspread.authorize(creds)
sheet = client.open('INDEC_RPI')

# get the first sheet of the Spreadsheet
sheet_instance = sheet.get_worksheet(0)

sheet_0 = sheet.get_worksheet(0)

def detect(frame):
    HOGCV = cv2.HOGDescriptor()                 
    HOGCV.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    bounding_box_cordinates, weights =  HOGCV.detectMultiScale(frame, winStride = (4, 4), padding = (8, 8), scale = 1.03)
    
    person = 1
    for x,y,w,h in bounding_box_cordinates:
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
        cv2.putText(frame, f'person {person}', (x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
        person += 1
    
    cv2.putText(frame, 'Status : Detecting ', (40,40), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2)
    cv2.putText(frame, f'Total Persons : {person-1}', (40,70), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2)
    cv2.imshow('output', frame)
    return person
    

     



 


 
# It is for removing/deleting created GUI window from screen
 

i=2
while True:
    if ser.in_waiting > 0:
            print('ok')
            indexa='A'+str(i)
            indexb='B'+str(i)
            indexc='C'+str(i)
            indexd='D'+str(i)
            indexe='E'+str(i)
            indexf='F'+str(i)
            indexg='G'+str(i)
            indexh='H'+str(i)
            indexi='I'+str(i)
            indexj='J'+str(i)
            indexk='K'+str(i)
            line = ser.readline().decode('utf-8').rstrip()
             
            if zzz==1:
                
                frame=cv2.imread('/home/pi/Desktop/indec_google sheets updation/3')
                frame = imutils.resize(frame , width=min(800,frame.shape[1]))
                print('Detecting people...')
                peop=detect(frame)
                cv2.destroyAllWindows()
                print(peop)
                zzz=0
            else:
                zzz=zzz+1
                
            if line=='ID read':
                i=1
            else:
                
                x=line.split(',')
                
                Hum=x[0]
                Tem=x[1]
                
                sheet_0.update_acell(indexa,str(Hum))
                sheet_0.update_acell(indexb,str(Tem))
                sheet_0.update_acell(indexc,x[2])
                sheet_0.update_acell(indexd,x[3])
                sheet_0.update_acell(indexe,x[4])
                sheet_0.update_acell(indexf,x[5])
                sheet_0.update_acell(indexg,x[6])
                sheet_0.update_acell(indexh,x[7])
                sheet_0.update_acell(indexi,peop-1)
                sheet_0.update_acell(indexj,str(randrange(0, 100)))
                sheet_0.update_acell(indexk,str(randrange(0, 100)))
                
                
                
                i=i+1
                 
                time.sleep(10)
                predicted=sheet_instance.get('M11')
                 
                sp=str(predicted[0])
                result = [val for val in sp if isinstance(val, (int, float))]
                ser.write(sp[3:5].encode('utf-8'))
                print(int(sp[3:5]))

