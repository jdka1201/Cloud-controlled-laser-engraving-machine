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

GPIO.setmode(GPIO.BCM)

gprs = 26
lack = 4
#success = 5
sucker = 23
suckerLR = 24
Materials = 25



GPIO.setup(sucker,GPIO.OUT)
GPIO.setup(suckerLR,GPIO.OUT)
GPIO.setup(Materials,GPIO.OUT)


GPIO.output(sucker,False)
GPIO.output(suckerLR,False)
GPIO.output(Materials,False)
#GPIO.setup(success,GPIO.IN)
GPIO.setup(gprs,GPIO.IN)
GPIO.setup(lack,GPIO.IN)

strss = ''
document = b''
a = ''

interface1_1 = b'\x65\x02\x02\x01'
interface1_2 = b'\x66\02'
interface2_1 = b'\x65\x02\x04\x01'
interface2_2 = b'\x66\04'
zero = b'\x65\x04\x08\x00'
suffix = b'\xFF\xFF\xFF'

time_pay = 120
time_pay_mark = 0
the_time = 0
disable = 0

ser = serial.Serial("/dev/ttyAMA0" , 9600)
ser_gprs = serial.Serial("/dev/ttyUSB0" , 9600)
if ser.isOpen == False:
    ser.open()
if ser_gprs.isOpen == False:
    ser_gprs.open()

from ui_Widget import Ui_Widget


def mov():
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
def mov2():
    global document
    ser.write(b'\x65\x02\x02\x01' + suffix + b'\x66\x02' + suffix)
    time.sleep(0.5)
    ser.write(b'\x65\x02' + document + b'\x01' + suffix )
    time.sleep(0.1)
    ser.write(b'\x65\x02\x06\x01' + suffix )
    time.sleep(0.1)
    
    
    GPIO.output(Materials,True)
    time.sleep(2)
    GPIO.output(Materials,False)
def mov1():
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
            time.sleep(0.1)
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
    time.sleep(11)
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
      self.ui.groupBox_wx.setGeometry(QtCore.QRect(250, 120, 0, 0))
      self.ui.groupBox_pay.setGeometry(QtCore.QRect(250, 70, 0, 0))
      self.ui.label_8.setGeometry(QtCore.QRect(90, 259, 0, 0))
      self.ui.widget_bu.setGeometry(QtCore.QRect(280, 80, 0, 0))
      self.ui.help_2.setGeometry(QtCore.QRect(810, 220, 0, 0))
      self.ui.pushButton_5.setGeometry(QtCore.QRect(130, 300, 0, 0))
      self.ui.pushButton_6.setGeometry(QtCore.QRect(10, 300, 0, 0))
      self.timer=QTimer()     #创建定时器
      self.timer.setInterval(1000)    #定时周期1000ms
      self.timer.timeout.connect(self.do_timer_timeout)

      GPIO.output(Materials,True)
      time.sleep(2)
      GPIO.output(Materials,False)
      self.timer1=QTimer()     #创建定时器
      self.timer1.setInterval(100)    #定时周期1000ms
      self.timer1.timeout.connect(self.do_timer1_timeout)
      self.timer1.start()
      #mooz initialize
      ser.write(interface2_1 + suffix + interface2_2 + suffix)
      time.sleep(0.5)
      ser.write(zero + suffix)
      time.sleep(13)
      
      ser.write(b'\x65\x02\x04\x01' + suffix + b'\x66\x04' + suffix)
      time.sleep(0.1)
      ser.write(b'\x65\x04\x07\x01' + suffix)    ## Z 07
      time.sleep(0.1)
      ser.write(b'\x71'+ b'\x0A' +b'\x00\x00\x00' + suffix)  ## Z
      time.sleep(2)
      
      global a
      show = 1
      f = open('/home/pi/mpython/data.txt','rb')
      a = f.read()
      #a = eval(a)
      f.close()
      
##  ==============自定义功能函数========================
   def paintEvent(self,event):  ##绘制窗口背景图片
      painter=QPainter(self)
      pic=QPixmap("1.jpg")
      painter.drawPixmap(0,0,self.width(),self.height(),pic)
      super().paintEvent(event)
      
      
   
##  ==============event处理函数==========================
   def on_help_released(self):
      global disable
      disable = 1
      self.ui.groupBox_wx.setGeometry(QtCore.QRect(250, 120, 291, 261))
   def on_pushButton__released(self):
      global disable
      disable = 0
      self.ui.groupBox_wx.setGeometry(QtCore.QRect(250, 120, 0, 0))
      
   def on_pushButton_released(self):
      global time_pay_mark
      global document
      time_pay_mark = 1
      document = b'\x0a'
      
   def on_pushButton_2_released(self):
      global time_pay_mark
      global document
      time_pay_mark = 1
      document = b'\x09'
       
   def on_pushButton_3_released(self):
      global time_pay_mark
      global document
      time_pay_mark = 1
      document = b'\x08'
       
   def on_pushButton_4_released(self):
      global time_pay_mark
      global document
      time_pay_mark = 1
      document = b'\x0b'
      
   def on_pushButton_qx_released(self):
      global time_pay_mark
      global disable
      disable = 0
      time_pay_mark = 0
      
      
##  ==========由connectSlotsByName()自动连接的槽函数============
   def do_timer_timeout(self):
      _translate = QtCore.QCoreApplication.translate
      self.ui.label_8.setText(_translate("Widget", "制作中，稍后..."))
      self.ui.widget_9.setStyleSheet("border-image: url(:/images/素材/images/25.png);")
      self.ui.label_7.setGeometry(QtCore.QRect(100, 20, 0, 0))
      self.ui.label_time_pay.setGeometry(QtCore.QRect(240, 20, 0, 0))
      self.ui.pushButton_qx.setGeometry(QtCore.QRect(150, 260, 0, 0))
      self.ui.label_8.setGeometry(QtCore.QRect(90, 259, 241, 31))
      self.timer.stop()
      print('123456')
      mov()
      mov2()
      print('789')
      
   def do_timer1_timeout(self):
      _translate = QtCore.QCoreApplication.translate
      global time_pay_mark
      global time_pay
      
      self.ui.time_n.setProperty("intValue", time.strftime('%Y',time.localtime(time.time())))
      self.ui.time_y_2.setProperty("intValue", time.strftime('%m',time.localtime(time.time())))
      self.ui.time_r.setProperty("intValue", time.strftime('%d',time.localtime(time.time())))
      #self.ui.time_h.setProperty("intValue", time.strftime('%H',time.localtime(time.time())))
      #self.ui.time_m.setProperty("intValue", time.strftime('%M',time.localtime(time.time())))

      self.ui.time_1.setText(_translate("Widget", time.strftime('%H',time.localtime(time.time()))))
      self.ui.time_2.setText(_translate("Widget", time.strftime('%M',time.localtime(time.time()))))
      if(time_pay_mark == 1):
         global disable
         global the_time
         disable = 1
         if (time_pay != 0):
            self.ui.groupBox_pay.setGeometry(QtCore.QRect(250, 70, 391, 331))
            self.ui.label_7.setGeometry(QtCore.QRect(100, 20, 131, 21))
            self.ui.label_time_pay.setGeometry(QtCore.QRect(240, 20, 51, 21))
            self.ui.pushButton_qx.setGeometry(QtCore.QRect(150, 260, 91, 31))
            self.ui.label_time_pay.setText(_translate("Widget",  str(time_pay)+'s'))
            the_time = the_time + 1
            if the_time >= 10:
                the_time = 0;
                time_pay = time_pay - 1
         else:
            time_pay_mark = 0
         size = ser_gprs.inWaiting()
         if size != 0:
             time.sleep(0.2)
             size = ser_gprs.inWaiting()
             response = ser_gprs.readline(size)
             print (response)
             ser_gprs.flushInput()
             if(response[0:16] == b'\xff\x00\x01\xdd'):
                 self.ui.label_7.setGeometry(QtCore.QRect(100, 20, 0, 0))
                 self.ui.label_time_pay.setGeometry(QtCore.QRect(240, 20, 0, 0))
                 self.ui.pushButton_qx.setGeometry(QtCore.QRect(150, 260, 0, 0))
                 self.ui.label_8.setGeometry(QtCore.QRect(90, 259, 241, 31))
                 self.ui.widget_9.setStyleSheet("border-image: url(:/images/素材/images/25.png);")
                 self.timer.start()
                 time_pay_mark = 2
         if GPIO.input(gprs) == True:
             self.ui.label_7.setGeometry(QtCore.QRect(100, 20, 0, 0))
             self.ui.label_time_pay.setGeometry(QtCore.QRect(240, 20, 0, 0))
             self.ui.pushButton_qx.setGeometry(QtCore.QRect(150, 260, 0, 0))
             self.ui.label_8.setGeometry(QtCore.QRect(90, 259, 241, 31))
             self.ui.widget_9.setStyleSheet("border-image: url(:/images/素材/images/25.png);")
             self.timer.start()
             time_pay_mark = 2
             
      elif(time_pay_mark == 0):
         time_pay = 120
         self.ui.groupBox_pay.setGeometry(QtCore.QRect(250, 70, 0, 0))
         self.ui.widget_9.setStyleSheet("border-image: url(:/images/素材/images/下载.png);")
         self.ui.label_8.setGeometry(QtCore.QRect(90, 259, 0, 0))
         if GPIO.input(lack) == True:
             disable = 1
             self.ui.widget_bu.setGeometry(QtCore.QRect(280, 80, 381, 261))
         else:
             disable = 0
             self.ui.widget_bu.setGeometry(QtCore.QRect(280, 80, 0, 0))
      elif(time_pay_mark == 2):
          size = ser.inWaiting()
          if size != 0:
              time.sleep(0.2)
              size = ser.inWaiting()
              response = ser.readline(size)
              print (response)
              ser.flushInput()
              if(response[0:8] == b't5.txt="'):
                  mov1()
                  time_pay_mark = 0
              
                         
      if(disable == 1):
         self.ui.pushButton.setEnabled(False)
         self.ui.pushButton_2.setEnabled(False)
         self.ui.pushButton_3.setEnabled(False)
         self.ui.pushButton_4.setEnabled(False)
      else:
         self.ui.pushButton.setEnabled(True)
         self.ui.pushButton_2.setEnabled(True)
         self.ui.pushButton_3.setEnabled(True)
         self.ui.pushButton_4.setEnabled(True)
         
         
         
      
      
        
        
##  =============自定义槽函数===============================        


   
##  ============窗体测试程序 ================================
if  __name__ == "__main__":        #用于当前窗体测试
   app = QApplication(sys.argv)    #创建GUI应用程序

   form=QmyWidget()                #创建窗体
   form.setWindowState(Qt.WindowFullScreen)
   form.show()

   sys.exit(app.exec_())
