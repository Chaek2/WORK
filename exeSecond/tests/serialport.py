from serial import Serial
import time

ser = Serial('COM5', baudrate=9600)

start = ["G21", "G90", "M82",
"G28 X0 Y0 Z0",
"G92 X0 Y0 Z0 E0"]

print(ser.isOpen())

for i in range(len(start)):
    print(start[i])
    ser.write(bytes(start[i], encoding=' utf-8'))
    time.sleep(3)

ser.close()

#light
#M804-5
#M806-7