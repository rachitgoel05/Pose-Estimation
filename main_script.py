#'''---------------TO RUN THE VIDEO FILES GRAB THE FIRST IMAGE OF THE VIDEOS &
#                  PROCESS THE IMAGE BY DEMO_IMAGE.PY AND SAVE THE IMAGE---------'''
import os
###
cwd=os.getcwd()

src_dir = (cwd+'/videos/outputs/')
dst_dir = (cwd+'/RESULTS/')
'''----------------TO PROCESS THE COMBINED IMAGE---------'''
os.chdir(cwd)
os.system('python demo_image.py --image ./RESULTS/processing2.jpg')


'''---------------------SCRIPT TO EXTRACT CORRDINATES----------------'''
import cv2
import pickle
with open(dst_dir+'parameters.data', 'rb') as filehandle:
    data = pickle.load(filehandle)
corr=[]
for i in range(0,len(data)):
    temp=[]
    for j in range(0,2):
        t=[]
        t.append(data[i][j][0])
        t.append(data[i][j][1])
        temp.append(t)
    corr.append(temp)
#print(corr)
#
'''---------------------SCRIPT TO DRAW LINES----------------'''
im_h=cv2.imread(dst_dir+'result.png')
for i in range(0,len(corr)):
    for j in range(0,2):
        im_h = cv2.circle(im_h, tuple(corr[i][j]), radius=4, color=(255,255,0), thickness=-1)
    
for i in range(0,len(corr)):
        im_h = cv2.line(im_h, tuple(corr[i][1]) ,tuple(corr[i][0]), color=(255,255,0), thickness=1)

cv2.imwrite(dst_dir+"final_result.jpg",im_h)

cv2.waitKey(100)
cv2.destroyAllWindows()

'''------------------LOGIC TO CHECK WEATHER THE PERSON IS SAME OR NOT---------'''


COCO_BODY_PARTS = ['nose', 'neck',
                   'right_shoulder', ' right_elbow', 'right_wrist',
                   'left_shoulder', 'left_elbow', 'left_wrist',
                   'right_hip', 'right_knee', 'right_ankle',
                   'left_hip', 'left_knee', 'left_ankle',
                   'right_eye', 'left_eye', 'right_ear', 'left_ear', 'background'
                   ]

print(corr)
diff_corr=[]
for i in range(0,len(corr)):
    diff_corr.append(abs(corr[i][1][1]-corr[i][0][1]))
per=0
count=0
for i in range(0,len(diff_corr)):
    if(diff_corr[i] <= 30):
        count+=1
per=(count/len(diff_corr))*100
print(per)
if per>0 and per<30:
    print("SLIGHT MATCH")
if per>31 and per<50:
    print("LESS THAN 50% MATCH")
if per>50 and per<80:
    print("SLIGHTLY MATCHED")
if(per>80):
    print("PERSON'S MATCH")
