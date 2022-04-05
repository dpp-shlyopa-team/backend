import serial
import time
ser = serial.Serial(port="COM7", baudrate=115200, bytesize=8, timeout=0.5, stopbits=serial.STOPBITS_ONE)
while True:
  s = ser.read(100)  # reading up to 100 bytes
  # s = str(s)[2:-5]
  print(s)
ser.close()
