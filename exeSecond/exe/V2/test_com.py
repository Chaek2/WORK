import pickle
class Setting:
    CAM = -1
    COM = 'COM'
camera_XY = [0,0]
box_first_XY = [0,0]
sets = Setting()
with open("exeSecond/exe/V2/ST/XYZ.pickle", "rb") as f:
    camera_XY = pickle.load(f)

with open("exeSecond/exe/V2/ST/BOX.pickle", "rb") as f:
    box_first_XY = pickle.load(f)

with open("exeSecond/exe/V2/ST/SET.pickle", "rb") as f:
    sets = pickle.load(f)

print(camera_XY)
print(box_first_XY)
print(sets.CAM,sets.COM)