import serial
import time
from datetime import datetime as dt

# make sure the 'COM#' is set according the Windows Device Manager
ser = serial.Serial('COM3', 9800, timeout=1)
time.sleep(5)

for i in range(50):
    line = ser.readline()   # read a byte
    if line:
        string = line.decode()  # convert the byte string to a unicode string
        try:
            tempc = float(string) # convert the unicode string to an int
        except:
            continue
        curr_time = dt.now()
        curr_time_str = curr_time.strftime("%Y:%m:%d %H:%M:%S")
        print(f'{curr_time_str}{tempc}')
ser.close()