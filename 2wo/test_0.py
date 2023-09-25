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

area1 = abs(((contr1[0][0]*contr1[1][1]-contr1[0][1]*contr1[1][0])+
         (contr1[1][0]*contr1[2][1]-contr1[1][1]*contr1[2][0])+
         (contr1[2][0]*contr1[3][1]-contr1[2][1]*contr1[3][0])+
         (contr1[3][0]*contr1[0][1]-contr1[3][1]*contr1[0][0]))/2)
area2 = abs(((contr2[0][0]*contr2[1][1]-contr2[0][1]*contr2[1][0])+
         (contr2[1][0]*contr2[2][1]-contr2[1][1]*contr2[2][0])+
         (contr2[2][0]*contr2[3][1]-contr2[2][1]*contr2[3][0])+
         (contr2[3][0]*contr2[0][1]-contr2[3][1]*contr2[0][0]))/2)

edge11 = np.int16((contr1[1][0] - contr1[0][0]+300,contr1[1][1] - contr1[0][1]+300))
edge21 = np.int16((contr1[2][0] - contr1[1][0]+300, contr1[2][1] - contr1[1][1]+300))

edge12 = np.int16((contr2[1][0] - contr2[0][0]+300,contr2[1][1] - contr2[0][1]+300))
edge22 = np.int16((contr2[2][0] - contr2[1][0]+300, contr2[2][1] - contr2[1][1]+300))
 
reference = (1,0) 

usedEdge1 = edge11
if cv.norm(edge21) > cv.norm(edge11):
    usedEdge1 = edge21

angle1 = 180.0/math.pi * math.acos((reference[0]*usedEdge1[0] + reference[1]*usedEdge1[1]) / (cv.norm(reference) *cv.norm(usedEdge1)))

usedEdge2 = edge12
if cv.norm(edge21) > cv.norm(edge12):
    usedEdge2 = edge21

angle2 = 180.0/math.pi * math.acos((reference[0]*usedEdge2[0] + reference[1]*usedEdge2[1]) / (cv.norm(reference) *cv.norm(usedEdge2)))

print(angle1)
print(angle2)