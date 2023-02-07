# -*- coding: utf-8 -*-

import sys
import time
import serial
import RPi.GPIO as GPIO
import binascii

from PyQt5 import QtCore
from PyQt5.QtWidgets import  QApplication, QWidget,QMessageBox
from PyQt5.QtCore import  pyqtSlot, Qt, QEvent
from PyQt5.QtCore import   QTime, QTimer
from PyQt5.QtGui import QPainter, QPixmap


from ui_Widget import Ui_Widget

GPIO.setmode(GPIO.BCM)

sucker = 23
suckerLR = 24
Materials = 25

sucker_io = 0
suckerLR_io = 0

GPIO.setup(sucker,GPIO.OUT)
GPIO.setup(suckerLR,GPIO.OUT)
GPIO.setup(Materials,GPIO.OUT)


GPIO.output(sucker,False)
GPIO.output(suckerLR,False)
GPIO.output(Materials,False)

show = 0
jg_show = 0
we = 0
strss = ''
X = ''
Y = ''
Z = ''
spot_ql = ''
spot_zl = ''
spot_cl = ''
spot_data = ''
a = ''

suffix = b'\xFF\xFF\xFF'
zero = b'\x65\x04\x08\x00'


ser = serial.Serial("/dev/ttyAMA0" , 9600)
if ser.isOpen == False:
    ser.open()

def mov():
    global we
    global a
    ############# X ##################
    X_100 = a.find(b'X')
    X_101 = a.find(b'.')
    X_110 = a[X_100 + 1 :X_101]
    ############# Y ##################
    Y_100 = a.find(b'Y')
    Y_101 = a.find(b'.',X_101+1)
    Y_110 = a[Y_100 + 1 :Y_101]
    ############# Z ##################
    Z_100 = a.find(b'Z')
    Z_101 = a.find(b'.',Y_101 + 1)
    Z_110 = a[Z_100 + 1 :Z_101]
    ############# X1 ##################
    X_200 = a.find(b'X',Z_100 + 1)
    X_201 = a.find(b'.',Z_101 + 1)
    X_210 = a[X_200 + 1 :X_201]
    ############# Y1 ##################
    Y_200 = a.find(b'Y',X_200 + 1)
    Y_201 = a.find(b'.',X_201 + 1)
    Y_210 = a[Y_200 + 1 :Y_201]
    ############# Z1 ##################
    Z_200 = a.find(b'Z',Y_200 + 1)
    Z_201 = a.find(b'.',Y_201 + 1)
    Z_210 = a[Z_200 + 1 :Z_201]
    print(Z_210)
    
##################### qld  #############################################################
    ############################### X #######################################
    if(a[X_100 + 1 : X_100 + 2 ] == b'-'):
        ser.write(b'\x65\x02\x04\x01' + suffix + b'\x66\x04' + suffix)
        time.sleep(0.1)
        ser.write(b'\x65\x04\x05\x01' + suffix)    ## X 05
        time.sleep(0.1)
        ser.write(b'\x71\x00\x00\x00\x00' + suffix)  ## X
        time.sleep(1)
        X_110 = a[X_100 + 2 :X_101]
        X_110 = int(X_110)
        while(X_110 > 0):
            ser.write(b'\x65\x02\x04\x01' + suffix + b'\x66\x04' + suffix)
            ser.write(b'\x65\x04\x0B\x01' + suffix)
            time.sleep(0.2)
            X_110 = X_110 - 1     
    else:
        print('no')
        X_110 = int(X_110)
        X_110 = hex(X_110)
        X_110 = str(X_110)
        X_110 = X_110[2:]
        if(len(X_110) <= 1):
            X_110 = "0" + X_110
        X_110 = binascii.a2b_hex(X_110)
        ser.write(b'\x65\x02\x04\x01' + suffix + b'\x66\x04' + suffix)
        time.sleep(0.1)
        ser.write(b'\x65\x04\x05\x01' + suffix)    ## X 05
        time.sleep(0.1)
        ser.write(b'\x71'+ X_110 +b'\x00\x00\x00' + suffix)  ## X
        time.sleep(2)
    ######################### Z #######################################
    if(a[Z_100 + 1 : Z_100 + 2 ] == b'-'):
        ser.write(b'\x65\x02\x04\x01' + suffix + b'\x66\x04' + suffix)
        time.sleep(0.1)
        ser.write(b'\x65\x04\x07\x01' + suffix)    ## Z 07
        time.sleep(0.1)
        ser.write(b'\x71\x00\x00\x00\x00' + suffix)  ## Z
        time.sleep(0.5)
        Z_110 = a[Z_100 + 2 :Z_101]
        Z_110 = int(Z_110) + 10
        while(Z_110 > 0):
            ser.write(b'\x65\x02\x04\x01' + suffix + b'\x66\x04' + suffix)
            ser.write(b'\x65\x04\x0D\x01' + suffix)
            time.sleep(0.1)
            Z_110 = Z_110 - 1
            print(Z_110)
    else:
        print('no')
        Z_110 = int(Z_110)
        Z_110 = hex(Z_110)
        Z_110 = str(Z_110)
        Z_110 = Z_110[2:]
        if(len(Z_110) <= 1):
            Z_110 = "0" + Z_110
        Z_110 = binascii.a2b_hex(Z_110)
        ser.write(b'\x65\x02\x04\x01' + suffix + b'\x66\x04' + suffix)
        time.sleep(0.1)
        ser.write(b'\x65\x04\x07\x01' + suffix)    ## Z 07
        time.sleep(0.1)
        ser.write(b'\x71'+ Z_110 +b'\x00\x00\x00' + suffix)  ## Z
        time.sleep(2)
    #####################   xp  #########################
    GPIO.output(suckerLR,True)
    time.sleep(0.1)
    GPIO.output(sucker,True)
    ##################### ZLD  ###########################
    ############################### Y #######################################
    Y_210 = int(Y_210)
    Y_210 = hex(Y_210)
    Y_210 = str(Y_210)
    Y_210 = Y_210[2:]
    if(len(Y_210) <= 1):
        Y_210 = "0" + Y_210
    Y_210 = binascii.a2b_hex(Y_210)
    ser.write(b'\x65\x02\x04\x01' + suffix + b'\x66\x04' + suffix)
    time.sleep(0.1)
    ser.write(b'\x65\x04\x06\x01' + suffix)    ## X 05
    time.sleep(0.1)
    ser.write(b'\x71'+ Y_210 +b'\x00\x00\x00' + suffix)  ## X
    time.sleep(1)
    ############################## Z #########################################
    ser.write(b'\x65\x02\x04\x01' + suffix + b'\x66\x04' + suffix)
    time.sleep(0.1)
    ser.write(b'\x65\x04\x07\x01' + suffix)    ## Z 07
    time.sleep(0.1)
    ser.write(b'\x71'+ b'\x0A' +b'\x00\x00\x00' + suffix)  ## Z
    time.sleep(2)
    ############################## X #########################################
    if(a[X_200 + 1 : X_200 + 2 ] == b'-'):
        ser.write(b'\x65\x02\x04\x01' + suffix + b'\x66\x04' + suffix)
        time.sleep(0.1)
        ser.write(b'\x65\x04\x05\x01' + suffix)    ## X 05
        time.sleep(0.1)
        ser.write(b'\x71\x00\x00\x00\x00' + suffix)  ## X
        time.sleep(2)
        X_210 = a[X_200 + 2 :X_201]
        X_210 = int(X_210)
        while(X_210 > 0):
            ser.write(b'\x65\x02\x04\x01' + suffix + b'\x66\x04' + suffix)
            ser.write(b'\x65\x04\x0B\x01' + suffix)
            time.sleep(0.2)
            X_210 = X_210 - 1     
    else:
        print('no')
        X_210 = int(X_210)
        X_210 = hex(X_210)
        X_210 = str(X_210)
        X_210 = X_210[2:]
        if(len(X_210) <= 1):
            X_210 = "0" + X_210
        X_210 = binascii.a2b_hex(X_210)
        ser.write(b'\x65\x02\x04\x01' + suffix + b'\x66\x04' + suffix)
        time.sleep(0.1)
        ser.write(b'\x65\x04\x05\x01' + suffix)    ## X 05
        time.sleep(0.1)
        ser.write(b'\x71'+ X_210 +b'\x00\x00\x00' + suffix)  ## X
        time.sleep(4)
    ############################ Z #############################################
    GPIO.output(Materials,False)
    time.sleep(1)
    GPIO.output(Materials,True)
    if(a[Z_200 + 1 : Z_200 + 2 ] == b'-'):
        ser.write(b'\x65\x02\x04\x01' + suffix + b'\x66\x04' + suffix)
        time.sleep(0.1)
        ser.write(b'\x65\x04\x07\x01' + suffix)    ## Z 07
        time.sleep(0.1)
        ser.write(b'\x71\x00\x00\x00\x00' + suffix)  ## Z
        time.sleep(2)
        Z_210 = a[Z_200 + 2 :Z_201]
        Z_210 = int(Z_210) + 10
        while(Z_210 > 0):
            ser.write(b'\x65\x02\x04\x01' + suffix + b'\x66\x04' + suffix)
            ser.write(b'\x65\x04\x0D\x01' + suffix)
            time.sleep(0.1)
            Z_210 = Z_210 - 1
            print(Z_210)
    else:
        print('no')
        Z_210 = int(Z_210)
        Z_210 = hex(Z_210)
        Z_210 = str(Z_210)
        Z_210 = Z_210[2:]
        if(len(Z_210) <= 1):
            Z_210 = "0" + Z_210
        Z_210 = binascii.a2b_hex(Z_210)
        ser.write(b'\x65\x02\x04\x01' + suffix + b'\x66\x04' + suffix)
        time.sleep(0.1)
        ser.write(b'\x65\x04\x07\x01' + suffix)    ## Z 07
        time.sleep(0.1)
        ser.write(b'\x71'+ Z_210 +b'\x00\x00\x00' + suffix)  ## Z
        time.sleep(2)    
    GPIO.output(suckerLR,False)
    GPIO.output(sucker,False)
    ############################## Z #########################################
    ser.write(b'\x65\x02\x04\x01' + suffix + b'\x66\x04' + suffix)
    time.sleep(0.1)
    ser.write(b'\x65\x04\x07\x01' + suffix)    ## Z 07
    time.sleep(0.1)
    ser.write(b'\x71'+ b'\x0A' +b'\x00\x00\x00' + suffix)  ## Z
    time.sleep(2)

def mov1():
    global we
    global a
    ############# X ##################
    X_100 = a.find(b'X')
    X_101 = a.find(b'.')
    X_110 = a[X_100 + 1 :X_101]
    ############# Y ##################
    Y_100 = a.find(b'Y')
    Y_101 = a.find(b'.',X_101+1)
    Y_110 = a[Y_100 + 1 :Y_101]
    ############# Z ##################
    Z_100 = a.find(b'Z')
    Z_101 = a.find(b'.',Y_101 + 1)
    Z_110 = a[Z_100 + 1 :Z_101]
    ############# X1 ##################
    X_200 = a.find(b'X',Z_100 + 1)
    X_201 = a.find(b'.',Z_101 + 1)
    X_210 = a[X_200 + 1 :X_201]
    ############# Y1 ##################
    Y_200 = a.find(b'Y',X_200 + 1)
    Y_201 = a.find(b'.',X_201 + 1)
    Y_210 = a[Y_200 + 1 :Y_201]
    ############# Z1 ##################
    Z_200 = a.find(b'Z',Y_200 + 1)
    Z_201 = a.find(b'.',Y_201 + 1)
    Z_210 = a[Z_200 + 1 :Z_201]
    ############# X2 ##################
    X_300 = a.find(b'X',Z_200 + 1)
    X_301 = a.find(b'.',Z_201 + 1)
    X_310 = a[X_300 + 1 :X_301]
    ############# Y2 ##################
    Y_300 = a.find(b'Y',X_300 + 1)
    Y_301 = a.find(b'.',X_301 + 1)
    Y_310 = a[Y_300 + 1 :Y_301]
    ############# Z2 ##################
    Z_300 = a.find(b'Z',Y_300 + 1)
    Z_301 = a.find(b'.',Y_301 + 1)
    Z_310 = a[Z_300 + 1 :Z_301]
    ##################### qLD  ###########################
    ############################### Y #######################################
    Y_210 = int(Y_210)
    Y_210 = hex(Y_210)
    Y_210 = str(Y_210)
    Y_210 = Y_210[2:]
    if(len(Y_210) <= 1):
        Y_210 = "0" + Y_210
    Y_210 = binascii.a2b_hex(Y_210)
    ser.write(b'\x65\x02\x04\x01' + suffix + b'\x66\x04' + suffix)
    time.sleep(0.1)
    ser.write(b'\x65\x04\x06\x01' + suffix)    ## X 05
    time.sleep(0.1)
    ser.write(b'\x71'+ Y_210 +b'\x00\x00\x00' + suffix)  ## X
    time.sleep(1)
    ############################## X #########################################
    if(a[X_300 + 1 : X_300 + 2 ] == b'-'):
        ser.write(b'\x65\x02\x04\x01' + suffix + b'\x66\x04' + suffix)
        time.sleep(0.1)
        ser.write(b'\x65\x04\x05\x01' + suffix)    ## X 05
        time.sleep(0.1)
        ser.write(b'\x71\x00\x00\x00\x00' + suffix)  ## X
        time.sleep(1)
        X_310 = a[X_300 + 2 :X_301]
        X_310 = int(X_310)
        while(X_310 > 0):
            ser.write(b'\x65\x02\x04\x01' + suffix + b'\x66\x04' + suffix)
            ser.write(b'\x65\x04\x0B\x01' + suffix)
            time.sleep(0.2)
            X_310 = X_310 - 1     
    else:
        print('no')
        X_310 = int(X_310)
        X_310 = hex(X_310)
        X_310 = str(X_310)
        X_310 = X_310[2:]
        if(len(X_310) <= 1):
            X_310 = "0" + X_310
        X_310 = binascii.a2b_hex(X_310)
        ser.write(b'\x65\x02\x04\x01' + suffix + b'\x66\x04' + suffix)
        time.sleep(0.1)
        ser.write(b'\x65\x04\x05\x01' + suffix)    ## X 05
        time.sleep(0.1)
        ser.write(b'\x71'+ X_310 +b'\x00\x00\x00' + suffix)  ## X
        time.sleep(4)
    ######################### Z #######################################
    if(a[Z_300 + 1 : Z_300 + 2 ] == b'-'):
        ser.write(b'\x65\x02\x04\x01' + suffix + b'\x66\x04' + suffix)
        time.sleep(0.1)
        ser.write(b'\x65\x04\x07\x01' + suffix)    ## Z 07
        time.sleep(0.1)
        ser.write(b'\x71\x00\x00\x00\x00' + suffix)  ## Z
        time.sleep(0.5)
        Z_310 = a[Z_300 + 2 :Z_301]
        Z_310 = int(Z_310) + 10
        while(Z_310 > 0):
            ser.write(b'\x65\x02\x04\x01' + suffix + b'\x66\x04' + suffix)
            ser.write(b'\x65\x04\x0D\x01' + suffix)
            time.sleep(0.1)
            Z_310 = Z_310 - 1
            print(Z_310)
    else:
        print('no')
        Z_310 = int(Z_310)
        Z_310 = hex(Z_310)
        Z_310 = str(Z_310)
        Z_310 = Z_310[2:]
        if(len(Z_310) <= 1):
            Z_310 = "0" + Z_310
        Z_310 = binascii.a2b_hex(Z_310)
        ser.write(b'\x65\x02\x04\x01' + suffix + b'\x66\x04' + suffix)
        time.sleep(0.1)
        ser.write(b'\x65\x04\x07\x01' + suffix)    ## Z 07
        time.sleep(0.1)
        ser.write(b'\x71'+ Z_310 +b'\x00\x00\x00' + suffix)  ## Z
        time.sleep(1)  
    GPIO.output(suckerLR,False)
    GPIO.output(sucker,True)
    ############################## Z #########################################
    ser.write(b'\x65\x02\x04\x01' + suffix + b'\x66\x04' + suffix)
    time.sleep(0.1)
    ser.write(b'\x65\x04\x07\x01' + suffix)    ## Z 07
    time.sleep(0.1)
    ser.write(b'\x71'+ b'\x0A' +b'\x00\x00\x00' + suffix)  ## Z
    time.sleep(1)
    ############################## X #########################################
    ser.write(b'\x65\x02\x04\x01' + suffix + b'\x66\x04' + suffix)
    time.sleep(0.1)
    ser.write(b'\x65\x04\x05\x01' + suffix)    ## X 05
    time.sleep(0.1)
    ser.write(b'\x71'+ b'\x6F' +b'\x00\x00\x00' + suffix)  ## X
    time.sleep(9)
    GPIO.output(suckerLR,False)
    GPIO.output(sucker,False)
    ser.write(b'\x65\x02\x04\x01' + suffix + b'\x66\x04' + suffix)
    time.sleep(0.1)
    ser.write(b'\x65\x04\x05\x01' + suffix)    ## X 05
    time.sleep(0.1)
    ser.write(b'\x71'+ b'\x2c' +b'\x00\x00\x00' + suffix)  ## X
    time.sleep(2)


class QmyWidget(QWidget): 

   def __init__(self, parent=None):
      super().__init__(parent)  #调用父类构造函数，创建窗体
      self.ui=Ui_Widget()       #创建UI对象
      self.ui.setupUi(self)     #构造UI界面
      _translate = QtCore.QCoreApplication.translate
      global show
      global a
      show = 1
      f = open('/home/pi/mpython/data.txt','rb')
      a = f.read()
      #a = eval(a)
      f.close()
      print(a)
      
      self.ui.label_04.setText(_translate("Widget", "OFF")) 
      self.ui.label_06.setGeometry(QtCore.QRect(120, 240, 33, 21))
      self.ui.label_01.setGeometry(QtCore.QRect(120, 40, 60, 21))
      self.ui.label_02.setGeometry(QtCore.QRect(120, 80, 60, 21))
      self.ui.label_03.setGeometry(QtCore.QRect(120, 120, 60, 21))
      self.ui.widget.setGeometry(QtCore.QRect(440, 80, 0, 0))
      
      ser.write(b'\x65\x02\x04\x01' + suffix + b'\x66\x04' + suffix)
      time.sleep(0.5)
      ser.write(zero + suffix)
      
      ser.write(b'\x65\x02\x04\x01' + suffix + b'\x66\x04' + suffix)
      time.sleep(0.1)
      ser.write(b'\x65\x04\x07\x01' + suffix)    ## Z 07
      time.sleep(0.1)
      ser.write(b'\x71'+ b'\x0A' +b'\x00\x00\x00' + suffix)  ## Z
      time.sleep(2)

      self.timer=QTimer()     
      self.timer.setInterval(1)    
      self.timer.timeout.connect(self.do_timer_timeout)
      self.timer.start()
      
      self.timer1=QTimer()    
      self.timer1.setInterval(250)  
      self.timer1.timeout.connect(self.do_timer1_timeout)
      #self.timer1.start()
##  ==============自定义功能函数========================
   def do_timer_timeout(self):
       global jg_show
       global P
       global we
       size = ser.inWaiting()
       if size != 0:
           self.timer.stop()
           self.timer1.start()
       if(jg_show == 1):
           ser.write(b'f\x03\xff\xff\xff')
           jg_show = 0
       if(we == 10):
           self.ui.widget.setGeometry(QtCore.QRect(440, 80, 0, 0))
           self.ui.groupBox_3.setEnabled(False)
           self.ui.groupBox_4.setEnabled(False)
           self.ui.groupBox_5.setEnabled(False)
           self.ui.preserve.setEnabled(False)
           self.ui.leave.setEnabled(False)
           self.ui.rest.setEnabled(False)
           self.ui.set_yd.setEnabled(False)
           self.ui.set_yd_2.setEnabled(False)
           self.ui.jg_off.setEnabled(False)
           self.ui.set_yd_3.setEnabled(False)
           self.ui.set_yd_4.setEnabled(False)
           #print('abc')
               
           
           
   def do_timer1_timeout(self):
       global show
       global jg_show
       global X
       global Y
       global Z
       global we
       _translate = QtCore.QCoreApplication.translate
       self.timer1.stop()
       size = ser.inWaiting()
       response = ser.readline(size)
       print (response)
       ser.flushInput()
       
       if(show == 1):
           if(response[0:8] == b't0.txt="'):
               X_we = response.find(b'X')
               Y_we = response.find(b'Y')
               Z_we = response.find(b'Z')
               D_we = response.find(b'"',Z_we)
               X = response[X_we + 1:Y_we - 1]
               Y = response[Y_we + 1:Z_we - 1]
               Z = response[Z_we + 1:D_we - 1]
               self.ui.label_01.setText(_translate("Widget", X))
               self.ui.label_02.setText(_translate("Widget", Y))
               self.ui.label_03.setText(_translate("Widget", Z))
               print(X)
               print(Y)
               print(Z)
               show = 0
       elif(show == 2):
           if(response[0:8] == b't0.txt="'):
               jg_p1 = response.find(b'"')
               jg_p2 = response.find(b'"',jg_p1+1)
               print(jg_p1)
               print(jg_p2)
               P = response[jg_p1 + 1:jg_p2 ]
               print(P)
               if(P == b'0'):
                   self.ui.label_05.setText(_translate("Widget", "OFF"))
               else:
                   self.ui.label_05.setText(_translate("Widget", "ON"))
               self.ui.label_06.setText(_translate("Widget", P))
               show = 0
       elif(show == 3):
           if(response[0:8] == b't5.txt="'):
               we = 0
               mov1()
               self.ui.groupBox_3.setEnabled(True)
               self.ui.groupBox_4.setEnabled(True)
               self.ui.groupBox_5.setEnabled(True)
               self.ui.preserve.setEnabled(True)
               self.ui.leave.setEnabled(True)
               self.ui.rest.setEnabled(True)
               self.ui.set_yd.setEnabled(True)
               self.ui.set_yd_2.setEnabled(True)
               self.ui.jg_off.setEnabled(True)
               self.ui.set_yd_3.setEnabled(True)
               self.ui.set_yd_4.setEnabled(True)
               show = 0
       elif(show == 5):
           if(response[0:8] == b't0.txt="'):
               X_we = response.find(b'X')
               Y_we = response.find(b'Y')
               Z_we = response.find(b'Z')
               D_we = response.find(b'"',Z_we)
               X = response[X_we + 1:Y_we - 1]
               Y = response[Y_we + 1:Z_we - 1]
               Z = response[Z_we + 1:D_we - 1]
               self.ui.label_01.setText(_translate("Widget", X))
               self.ui.label_02.setText(_translate("Widget", Y))
               self.ui.label_03.setText(_translate("Widget", Z))
               print(X)
               print(Y)
               print(Z)
               global spot_ql
               spot_ql =  b'X'+X + b'Y'+ Y + b'Z' + Z
               print(spot_ql)
               show = 0
       elif(show == 6):
           if(response[0:8] == b't0.txt="'):
               X_we = response.find(b'X')
               Y_we = response.find(b'Y')
               Z_we = response.find(b'Z')
               D_we = response.find(b'"',Z_we)
               X = response[X_we + 1:Y_we - 1]
               Y = response[Y_we + 1:Z_we - 1]
               Z = response[Z_we + 1:D_we - 1]
               self.ui.label_01.setText(_translate("Widget", X))
               self.ui.label_02.setText(_translate("Widget", Y))
               self.ui.label_03.setText(_translate("Widget", Z))
               print(X)
               print(Y)
               print(Z)
               global spot_zl
               spot_zl =  b'X'+X + b'Y'+ Y + b'Z' + Z
               print(spot_zl)
               show = 0
       elif(show == 7):
           if(response[0:8] == b't0.txt="'):
               X_we = response.find(b'X')
               Y_we = response.find(b'Y')
               Z_we = response.find(b'Z')
               D_we = response.find(b'"',Z_we)
               X = response[X_we + 1:Y_we - 1]
               Y = response[Y_we + 1:Z_we - 1]
               Z = response[Z_we + 1:D_we - 1]
               self.ui.label_01.setText(_translate("Widget", X))
               self.ui.label_02.setText(_translate("Widget", Y))
               self.ui.label_03.setText(_translate("Widget", Z))
               print(X)
               print(Y)
               print(Z)
               global spot_cl
               spot_cl =  b'X'+X + b'Y'+ Y + b'Z' + Z
               print(spot_cl)
               show = 0
       self.timer.start()
           
       

        
##  =============自定义槽函数===============================        
   def on_x_subtract_released(self):
      global show
      show = 1
      print('x -')
      ser.write(b'\x65\x02\x04\x01' + suffix + b'\x66\x04' + suffix)
      #time.sleep(0.1)
      ser.write(b'\x65\x04\x0B\x01' + suffix)

   def on_x_add_released(self):
      global show
      show = 1
      print('x +')
      ser.write(b'\x65\x02\x04\x01' + suffix + b'\x66\x04' + suffix)
      #time.sleep(0.2)
      ser.write(b'\x65\x04\x0E\x01' + suffix)
      
   def on_y_subtract_released(self):
      global show
      show = 1 
      print('y -')
      ser.write(b'\x65\x02\x04\x01' + suffix + b'\x66\x04' + suffix)
      #time.sleep(0.2)
      ser.write(b'\x65\x04\x0C\x01' + suffix)
      
   def on_y_add_released(self):
      global show
      show = 1
      print('y +')
      ser.write(b'\x65\x02\x04\x01' + suffix + b'\x66\x04' + suffix)
      #time.sleep(0.2)
      ser.write(b'\x65\x04\x0F\x01' + suffix)
      
   def on_z_subtract_released(self):
      global show
      show = 1
      print('z -')
      ser.write(b'\x65\x02\x04\x01' + suffix + b'\x66\x04' + suffix)
      #time.sleep(0.2)
      ser.write(b'e\x04\r\x01\xff\xff\xff')
      
   def on_z_add_released(self):
      global show
      show = 1
      print('z +')
      ser.write(b'\x65\x02\x04\x01' + suffix + b'\x66\x04' + suffix)
      #time.sleep(0.2)
      ser.write(b'e\x04\x10\x01\xff\xff\xff')

   def on_jg_on_released(self):
      global show
      global jg_show
      show = 2
      ser.write(b'\x65\x03\x0a\x01' + suffix )
      print('jg_off')
      jg_show = 1
      
   def on_jg_off_released(self):
      
      print('jg_off')

      
   def on_p_subtract_released(self):
      global show
      global jg_show
      jg_show = 1
      show = 2
      
      ser.write(b'\x65\x03\x06\x01' + suffix)
      
      print('jg_--')
   def on_p_add_released(self):
      global show
      global jg_show
      jg_show = 1
      show = 2
     
      ser.write(b'\x65\x03\x07\x01' + suffix)
 
      print('jg_++')

   def on_jg_on_2_released(self):
      global sucker_io
      _translate = QtCore.QCoreApplication.translate
      if(sucker_io == 0):
          self.ui.label_04.setText(_translate("Widget", "ON"))
          GPIO.output(sucker,True)
          sucker_io = 1
      elif(sucker_io == 1):
          self.ui.label_04.setText(_translate("Widget", "OFF"))
          GPIO.output(sucker,False)
          sucker_io = 0
      
      
   def on_jg_off_2_released(self):
      global suckerLR_io
      if(suckerLR_io == 0):
          GPIO.output(suckerLR,True)
          suckerLR_io = 1
      elif(suckerLR_io == 1):
          GPIO.output(suckerLR,False)
          suckerLR_io = 0


   def on_rest_released(self):
      global show
      show = 1
      print('rest')
      ser.write(b'\x65\x02\x04\x01' + suffix + b'\x66\x04' + suffix)
      time.sleep(0.5)
      ser.write(b'e\x04\x08\x00\xff\xff\xff')
      
   def on_set_yd_released(self):
      global show
      show = 1
      print('set_yd')
      ser.write(b'\x65\x02\x04\x01' + suffix + b'\x66\x04' + suffix)
      time.sleep(0.5)
      ser.write(b'\x65\x04\x0A\x00' + suffix)
      
   def on_set_yd_2_released(self):
      global show
      show = 5
      print('qld')
      ser.write(b'\x65\x02\x04\x01' + suffix + b'\x66\x04' + suffix)
      ser.write(b'\x65\x04\x10\x01' + suffix)

    
   def on_jg_off_released(self):
      global show
      show = 6
      print('zld')
      ser.write(b'\x65\x02\x04\x01' + suffix + b'\x66\x04' + suffix)
      ser.write(b'\x65\x04\x10\x01' + suffix)
      
   def on_set_yd_3_released(self):
      global show
      show = 7
      print('cld')
      ser.write(b'\x65\x02\x04\x01' + suffix + b'\x66\x04' + suffix)
      ser.write(b'\x65\x04\x10\x01' + suffix)
      
   def on_set_yd_4_released(self):
      self.ui.widget.setGeometry(QtCore.QRect(440, 80, 181, 141))
      
      
      #self.ui.groupBox_3.setEnabled(False)
   def on_tu1_released(self):
      print('preserve')
      global show
      global we
      mov()
      ser.write(b'\x65\x02\x02\x01' + suffix + b'\x66\x02' + suffix)
      time.sleep(0.5)
      ser.write(b'\x65\x02\x08\x01' + suffix )
      time.sleep(0.1)
      ser.write(b'\x65\x02\x06\x01' + suffix )
      time.sleep(0.1)
      show = 3
      we = 10
      
      
   def on_tu2_released(self):
      print('preserve')
      global show
      global we
      mov()
      ser.write(b'\x65\x02\x02\x01' + suffix + b'\x66\x02' + suffix)
      time.sleep(0.5)
      ser.write(b'\x65\x02\x09\x01' + suffix )
      time.sleep(0.1)
      ser.write(b'\x65\x02\x06\x01' + suffix )
      time.sleep(0.1)
      show = 3
      we = 10
   def on_tu3_released(self):
      print('preserve')
      global show
      global we
      mov()
      ser.write(b'\x65\x02\x02\x01' + suffix + b'\x66\x02' + suffix)
      time.sleep(0.5)
      ser.write(b'\x65\x02\x0a\x01' + suffix )
      time.sleep(0.1)
      ser.write(b'\x65\x02\x06\x01' + suffix )
      time.sleep(0.1)
      show = 3
      we = 10
   def on_tu4_released(self):
      print('preserve')
      global show
      global we
      mov()
      ser.write(b'\x65\x02\x02\x01' + suffix + b'\x66\x02' + suffix)
      time.sleep(0.5)
      ser.write(b'\x65\x02\x0b\x01' + suffix )
      time.sleep(0.1)
      ser.write(b'\x65\x02\x06\x01' + suffix )
      time.sleep(0.1)
      show = 3
      we = 10
   def on_preserve_released(self):
      global spot_ql
      global spot_zl
      global spot_cl
      global spot_data
      spot_data = (spot_ql + b',' + spot_zl + b',' + spot_cl)
      f = open('/home/pi/mpython/data.txt','wb')
      f.write(spot_data)
      f.close()
      print(spot_data)

   

   
   
   
##  ============窗体测试程序 ================================
if  __name__ == "__main__":        #用于当前窗体测试
   app = QApplication(sys.argv)    #创建GUI应用程序

   form=QmyWidget()                #创建窗体
   form.show()

   sys.exit(app.exec_())


