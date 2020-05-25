# based on: https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_feature2d/py_feature_homography/py_feature_homography.html
import cv2
import numpy as np
import matplotlib.pyplot as plt
MIN_MATCH_COUNT = 10
FLANN_INDEX_KDTREE = 1  

# read the images
model_image = cv2.imread('homealone1.jpg' ,0)
input_image = cv2.imread('homealone101.jpg' ,0)

# --------- SIFT FEATURE DETETCION & DESCRIPTION ------------------------
# Initiate SIFT detector. Alternatives are SURF, ORB, BRIEF, ...
sift = cv2.xfeatures2d.SIFT_create()
# find the keypoints and descriptors with SIFT
kp_model, des_model = sift.detectAndCompute(model_image,None) # returns keypoints and descriptors
kp_input, des_input = sift.detectAndCompute(input_image,None)

# --------- FEATURE MATCHING : FLANN MATCHER -------------------
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks = 50)
flann = cv2.FlannBasedMatcher(index_params, search_params)
matches = flann.knnMatch(des_model,des_input,k=2)

# store all the good matches as per Lowe's ratio test.
good = []
for m,n in matches:
    if m.distance < 0.80*n.distance:
        good.append(m)

if len(good)>MIN_MATCH_COUNT:
    model_pts = np.float32([ kp_model[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
    input_pts = np.float32([ kp_input[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

    # Find only the good, corresponding points (lines of matching points may not cross)
    # Returns the perspective transformation matrix M
    M, mask = cv2.findHomography(input_pts, model_pts, cv2.RANSAC,5.0)  #tresh : 5

    matchesMask = mask.ravel().tolist()
    h,w = model_image.shape

    # the square that's drawn on the model. Just the prerspective transformation of the model image contours
    pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
    dst = cv2.perspectiveTransform(pts,M)

    perspective_transform_input = cv2.warpPerspective(input_image, M, (w, h ))
    plt.figure()
    plt.subplot(131), plt.imshow(model_image), plt.title('Model')
    plt.subplot(132), plt.imshow(perspective_transform_input), plt.title('Perspective transformed Input')
    plt.subplot(133), plt.imshow(input_image), plt.title('Input')
    plt.show(block=False)

    input_image_homo = cv2.polylines(input_image,[np.int32(dst)],True,255,3, cv2.LINE_AA)  # draw homography square
    #model_image_homo = cv2.polylines(model_image, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)  # draw homography square

    print (matchesMask, input_image_homo, good, model_pts, input_pts, M)
    #return (matchesMask, model_image_homo, good, model_pts, input_pts)

else:
    print( "Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT) )
    matchesMask = None
    print ("not found")