import argparse
import time
import os
import cv2
import math

from processing import extract_parts, draw

from config_reader import config_reader
from model.cmu_model import get_testing_model
parts=["nose", "neck", "Rsho", "Relb", "Rwri", "Lsho", "Lelb", "Lwri", "Rhip", "Rkne", "Rank", "Lhip", "Lkne", "Lank", "Leye", "Reye", "Lear", "Rear"]
points={}
for i in parts:
    points[i]=0
files=os.listdir("D:\minor2\\video2\cycle2-")
sets=[]

def slope(x1,y1,x2,y2):
    return((y1-y2)/(x2-x1))


def getAngle(x1,y1,x2,y2,x3,y3):
    # m1=math.degrees(math.atan(slope(x1,y1,x2,y2)))
    # m2=math.degrees(math.atan(slope(x2,y2,x3,y3)))
    # angle=math.fabs(m1-m2)
    # print(angle)
    X1=x1-x2
    Y1=y1-y2
    X2=x3-x2
    Y2=y3-y2
    ans=((X1*X2)+(Y1*Y2))/(math.sqrt(math.pow(X1,2)+math.pow(Y1,2))*math.sqrt(math.pow(X2,2)+math.pow(Y2,2)))
    ans=math.acos(ans)
    ans=math.degrees(ans)
    print(ans)


def getLegLength(x1,y1,x2,y2,x3,y3):

    l1=math.sqrt(math.pow(x2-x1,2)+math.pow(y2-y1,2))

    l2=math.sqrt(math.pow(x2-x3,2)+math.pow(y2-y3,2))
    print(l1+l2)

def getStepLength(x1,y1,x2,y2):
    l=math.sqrt(math.pow(x2-x1,2)+math.pow(y2-y1,2))
    print(l)

for i in files:

    if __name__ == '__main__':
        

        image_path = "D:\minor2\\video2\cycle2-\\"+i
        output = "D:\minor2\\video2\cycle2-\\"+i[0:-4]+"result"+i[-4:]
        keras_weights_file = 'model/keras/model.h5'

        tic = time.time()
        print('start processing...')

        # load model

        # authors of original model don't use
        # vgg normalization (subtracting mean) on input images
        model = get_testing_model()
        model.load_weights(keras_weights_file)

        # load config
        params, model_params = config_reader()
        
        input_image = cv2.imread(image_path)  # B,G,R order
        
        all_peaks, subset, candidate = extract_parts(input_image, params, model, model_params)
        canvas = draw(input_image, all_peaks, subset, candidate)
        cv2.imwrite(output, canvas)
        cv2.destroyAllWindows()
        # print(all_peaks)
        for i in range(len(all_peaks)):
            if(parts[i] in ['Lhip','Rhip','Lkne','Rkne','Lank','Rank']):
                try:
                    if(len(all_peaks[i])>1 ):
                        print(parts[i],all_peaks[i])
                        ind=input()
                        points[parts[i]]=all_peaks[i][int(ind)]
                        print(parts[i],all_peaks[i][int(ind)])
                    elif(len(all_peaks[i])==0):
                        print(parts[i]," has zero points")
                        continue
                    else:
                        points[parts[i]]=all_peaks[i][0]
                        print(parts[i],points[parts[i]])
                except IndexError:
                    print("error",i,len(parts),parts,all_peaks[i])
            
        print(points['Lhip'],points['Rhip'],points['Lank'],points['Rank'])
        sets.append([points['Lhip'],points['Rhip'],points['Lkne'],points['Rkne'],points['Lank'],points['Rank']])

        
        toc = time.time()
        print('processing time is %.5f' % (toc - tic))
print(sets)
for i in range(3):
    Lhip=sets[i][0]
    Rhip=sets[i][1]
    Lkne=sets[i][2]
    Rkne=sets[i][3]
    Lank=sets[i][4]
    Rank=sets[i][5]
    getAngle(Lank[0],Lank[1],Lhip[0],Lhip[1],Rank[0],Rank[1])
    getAngle(Lank[0],Lank[1],Rhip[0],Rhip[1],Rank[0],Rank[1])
    getLegLength(Lank[0],Lank[1],Lkne[0],Lkne[1],Lhip[0],Lhip[1])
    getLegLength(Rank[0],Rank[1],Rkne[0],Rkne[1],Rhip[0],Rhip[1])
    getStepLength(Lank[0],Lank[1],Rank[0],Rank[1])
    print("--------------------")
    if(i==0):
        sli=Rank[0]
        sly=Rank[1]
    if(i==2):
        getStepLength(sli,sly,Rank[0],Rank[1])
    