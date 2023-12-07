import pickle
class Setting:
    CAM = -1
    COM = 'COM'
camera_XY = [0,0]
box_first_XY = [0,0]
sets = Setting()
with open("XYZ.pickle", "rb") as f:
    camera_XY = pickle.load(f)

with open("BOX.pickle", "rb") as f:
    box_first_XY = pickle.load(f)

with open("SET.pickle", "rb") as f:
    sets = pickle.load(f)

print(camera_XY)
print(box_first_XY)
print(sets.CAM,sets.COM)