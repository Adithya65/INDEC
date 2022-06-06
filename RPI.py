import cv2
import imutils
import numpy as np
import argparse
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import serial
import time
line=[]


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
    

     



frame=cv2.imread('/home/pi/Desktop/indec_google sheets updation/bb')
frame = imutils.resize(frame , width=min(800,frame.shape[1]))
print('Detecting people...')
peop=detect(frame)
 


 
# It is for removing/deleting created GUI window from screen
# and memory
cv2.destroyAllWindows()
i=2
while True:
    if ser.in_waiting > 0:
            indexa='A'+str(i)
            indexb='B'+str(i)
            indexc='C'+str(i)
            line = ser.readline().decode('utf-8').rstrip()
             
            Hum=line[0:5]
            Tem=line[5:10]
            sheet_0.update_acell(indexa,str(Hum))
            sheet_0.update_acell(indexb,str(Tem))
            sheet_0.update_acell(indexc,peop)
            
            i=i+1
            print(Hum)
            time.sleep(10)
