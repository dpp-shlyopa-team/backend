import serial
import time
ser = serial.Serial(port="COM8", baudrate=115200, bytesize=8, timeout=5, stopbits=serial.STOPBITS_ONE)
while True:
  s = ser.read(1000)  # reading up to 100 bytes
  # print(str(s)[2:-5].replace('\\r\\n', '\n'))
  s = str(s)[2:-5].split('\\r\\n')
  r = {}
  for i in s:
    i = i.split(': ')
    if (len(i) > 1):
      r[i[0]] = i[1]
  print(r)
ser.close()