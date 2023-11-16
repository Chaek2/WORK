import engine, keyboard,time
import cv2 as cv

x=float(0)
y=float(0)

while 1:
    command = input("Command:  ")
    if command == 'EXIT':
        break
    engine.perform(command)
        
#CAMERA DOWN
#G0 X60.4 Y171 Z10

# engine.com_port('G0 A90') - A поворот
# engine.com_port('G0 X90') - X ось
# engine.com_port('G0 Y90') - Y ось
# engine.com_port('G0 Z90') - Z ось


#light
#M804-5 on/of up
#M806-7 on/off down


