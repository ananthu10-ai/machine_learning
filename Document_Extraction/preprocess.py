# import the necessary packages
from PIL import Image
import cv2
import time
import numpy as np
from binarization import nlbin


################################################################################################################
############################# Section 1: Initiate the command line interface ###################################
################################################################################################################

# construct the argument parse and parse the arguments
def process_image(image_path):
    start_time_bin = time.time()
    image = Image.open(image_path)
    array = np.array(image)
    h,w,_ =array.shape
    array = array[:,:int(0.7*w),:]
    crop_img = Image.fromarray(array).convert("L")
    img_bin = nlbin(crop_img)
    end_time_bin = time.time()
    final_time_bin = end_time_bin - start_time_bin
    print("########################################################################################")
    print("time to first binarization image  ", final_time_bin)
    print("#########################################################################################")
    return img_bin
##############################################################################################################
######################       Section 4:	CROP PAN                                      ########################
##############################################################################################################












