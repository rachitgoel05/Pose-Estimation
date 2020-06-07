import os
import sys
import argparse
import cv2
import time

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--video', type=str, required=True, help='input video file name')
    parser.add_argument('--model', type=str, default='model/keras/model.h5', help='path to the weights file')
    parser.add_argument('--frame_ratio', type=int, default=1, help='analyze every [n] frames')
    parser.add_argument('--process_speed', type=int, default=4,
                        help='Int 1 (fastest, lowest quality) to 4 (slowest, highest quality)')
    parser.add_argument('--end', type=int, default=None, help='Last video frame to analyze')
    args = parser.parse_args()
    frame_rate_ratio = args.frame_ratio
    process_speed = args.process_speed
    ending_frame = args.end
    print('start processing...')

    # Video input
    video = args.video
    video_path = 'videos/'
    video_file = video_path + video
    # Output location
    output_path = 'videos/outputs/'
    output_format = '.mp4'
    video_output = output_path + video  + output_format
    cam = cv2.VideoCapture(video_file)
    input_fps = cam.get(cv2.CAP_PROP_FPS)
    ret_val, orig_image = cam.read()
    video_length = int(cam.get(cv2.CAP_PROP_FRAME_COUNT))
    if ending_frame is None:
        ending_frame = video_length
    i = 0  # default is 0
    count=0
    numbers=0
    while (cam.isOpened()) and ret_val is True and i < ending_frame:
        if i % frame_rate_ratio == 0:
            ret_val, orig_image = cam.read()
            if(ret_val):
                cv2.imwrite(output_path + "skeleton"+str(count)+".jpg",canvas)
                count+=1
                print("Image Saved")
        i+=1
cam.release()
        