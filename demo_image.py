import argparse
import time
import os
import cv2
import pickle
from processing import extract_parts, draw

from config_reader import config_reader
from model.cmu_model import get_testing_model

if __name__ == '__main__':
    cwd=os.getcwd()
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', type=str, required=True, help='input image')
    parser.add_argument('--output', type=str, default=(cwd+'/RESULTS/result.png'), help='output image')
    parser.add_argument('--model', type=str, default='model/keras/model.h5', help='path to the weights file')

    args = parser.parse_args()
    image_path = args.image
    output = args.output
    keras_weights_file = args.model

    tic = time.time()
    print('start processing...')

    # load model

    # authors of original model don't use
    # vgg normalization (subtracting mean) on input images
    model = get_testing_model()
    model.load_weights(keras_weights_file)

    # load config
    params, model_params = config_reader()
    print("params",params,"\n")
    print(output)
    input_image = cv2.imread(image_path)  # B,G,R order
    
    all_peaks, subset, candidate = extract_parts(input_image, params, model, model_params)
    canvas = draw(input_image, all_peaks, subset, candidate)
    toc = time.time()
    cv2.imwrite(output, canvas)
    cwd=os.getcwd()
    print(all_peaks)
    des_dir=cwd+'/RESULTS/'
    with  open((des_dir+'parameters.data'),'wb') as file:
        pickle.dump(all_peaks,file)
    cv2.destroyAllWindows()



