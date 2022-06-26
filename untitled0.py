# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rLb84aK-1A2e74zPyMhg3i0i6uqp68oq
"""

import pandas as pd
import numpy as np
import matplotlib_inline
import seaborn as sn
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.model_selection import train_test_split
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import time
from google.colab import drive

#file=pd.read_csv("/content/Indec2_jun5_F - Sheet1.csv")
drive.mount('/content/drive')
datafile=pd.read_csv("/content/drive/MyDrive/INDEC/Indec2_jun5_F - Sheet1.csv")
X=datafile[["Air Velocity","Ini_Temp","Humidity","ambL","Nofpeop","AQI","Pressure","RoomA"]]
y=datafile["AC Temperature"]
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 1)
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('/content/drive/MyDrive/INDEC/indec1-62dee87066a5.json', scope)

# authorize the clientsheet 
client = gspread.authorize(creds)
sheet = client.open('INDEC_RPI')

# get the first sheet of the Spreadsheet
sheet_instance = sheet.get_worksheet(0)

lin = LinearRegression()
lin.fit(X, y)

i=2
check=0
while True:
  indexa='A'+str(i)
  indexh='H'+str(i)
  mer=indexa+':'+indexh
  check=sheet_instance.get('A'+str(i))
  if check==[['0']]:
    time.sleep(10)
    print(1)

  else:
    aa=sheet_instance.get(mer)
    x=(lin.predict(aa) )
    i=i+1
    sheet_instance.update_acell('k11',str(x))