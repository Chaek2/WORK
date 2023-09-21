import math
import numpy as np
import cv2 as cv

contr1 = [[576,789],
          [640,732],
          [666,761],
          [602,818]]

contr2 = [[442,621],
          [506,562],
          [532,590],
          [468,649]]

contr3 = [[470,643],
          [712,480],
          [787,592],
          [545,754]]

area1 = abs(((contr1[0][0]*contr1[1][1]-contr1[0][1]*contr1[1][0])+
         (contr1[1][0]*contr1[2][1]-contr1[1][1]*contr1[2][0])+
         (contr1[2][0]*contr1[3][1]-contr1[2][1]*contr1[3][0])+
         (contr1[3][0]*contr1[0][1]-contr1[3][1]*contr1[0][0]))/2)
area2 = abs(((contr2[0][0]*contr2[1][1]-contr2[0][1]*contr2[1][0])+
         (contr2[1][0]*contr2[2][1]-contr2[1][1]*contr2[2][0])+
         (contr2[2][0]*contr2[3][1]-contr2[2][1]*contr2[3][0])+
         (contr2[3][0]*contr2[0][1]-contr2[3][1]*contr2[0][0]))/2)
area3 = abs(((contr3[0][0]*contr3[1][1]-contr3[0][1]*contr3[1][0])+
         (contr3[1][0]*contr3[2][1]-contr3[1][1]*contr3[2][0])+
         (contr3[2][0]*contr3[3][1]-contr3[2][1]*contr3[3][0])+
         (contr3[3][0]*contr3[0][1]-contr3[3][1]*contr3[0][0]))/2)
print(area1)
print(area2)
print(area3)

edge11 = np.int0((contr1[1][0] - contr1[0][0]+300,contr1[1][1] - contr1[0][1]+300))
edge21 = np.int0((contr1[2][0] - contr1[1][0]+300, contr1[2][1] - contr1[1][1]+300))

edge12 = np.int0((contr2[1][0] - contr2[0][0]+300,contr2[1][1] - contr2[0][1]+300))
edge22 = np.int0((contr2[2][0] - contr2[1][0]+300, contr2[2][1] - contr2[1][1]+300))

edge13 = np.int0((contr3[1][0] - contr3[0][0]+300,contr3[1][1] - contr3[0][1]+300))
edge23 = np.int0((contr3[2][0] - contr3[1][0]+300, contr3[2][1] - contr3[1][1]+300))

 