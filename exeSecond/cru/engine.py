import os, time

com_port="COM5"

start = ["G21",
"G90",
"M82",
"G28 X0 Y0 Z0",
"G92 X0 Y0 Z0 E0"]

mode = os.popen('mode '+com_port).read()

if len(mode) < 100:
    print('Ошибка с подключением с портом')
    quit()

print('start')

try:
    time.sleep(1)
    m = os.popen('echo '+start[0]+' > '+com_port).read()
    time.sleep(1)
    m = os.popen('echo '+start[1]+' > '+com_port).read()
    time.sleep(1)
    m = os.popen('echo '+start[2]+' > '+com_port).read()
    time.sleep(1)
    m = os.popen('echo '+start[3]+' > '+com_port).read()
    time.sleep(3)
    m = os.popen('echo '+start[4]+' > '+com_port).read()
    time.sleep(1)
except Exception as e:
    print(e)

def perform(arr):
    try:
        m = os.popen('echo '+arr.upper()+' > '+com_port).read()
        return m
    except Exception as e:
        print(e)
        return e

