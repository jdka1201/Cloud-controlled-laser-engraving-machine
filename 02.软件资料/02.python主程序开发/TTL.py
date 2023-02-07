import serial
ser = serial.Serial("/dev/ttyUSB0" , 9600)
if ser.isOpen == False:
    ser.open()

while(True):
    size = ser.inWaiting()
    if size != 0:
        size = ser.inWaiting()
        response = ser.readline(size)
        print (response)
        ser.flushInput()
    