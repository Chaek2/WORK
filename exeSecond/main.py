import engine, keyboard,time
import cv2 as cv

x=float(0)
y=float(0)

while 1:
    command = input("Command:  ")
    if command == 'EXIT':
        break
    engine.move_axis(command)
    
#62 171 - CAMERA DOWN
#G0 X62 Y171
#G0 X60.4 Y170.8

# engine.com_port('G0 A90') - поворот
# engine.com_port('G0 X90') - X
# engine.com_port('G0 Y90') - Y
# engine.com_port('G0 Z90') - Z
