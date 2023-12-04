import engine

engine.start("COM5")

while 1:
    command = input("Command: ")
    if command == "EX":
        break
    engine.perform("G0 "+command)
    input("END? ")
    engine.perform("G0 X0 Y0 Z0")
        
