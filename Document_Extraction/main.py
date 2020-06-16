import os 
import re 
from  preprocess import process_image
import numpy as np
from panfinal import pan_fill
from PIL import Image
import pytesseract
import cv2
import time


def main():
    image_path = "/home/ananthu/projects/Document_Extraction/data/pan_16.jpg"
    binarized_image = process_image(image_path)
    binarized_image.save("pan.png")
    x = pytesseract.image_to_string(binarized_image)
    id_read("pan.png")
    data = pan_fill(x)



def id_read(croped_image_path):
	mycommand = 'tesseract' + ' ' + croped_image_path + ' ' + 'idtext' + ' ' 
	os.system(mycommand)
main()
