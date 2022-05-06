import cv2 
import matplotlib.pyplot as plt
import numpy as np

def get_flag_color(img):
    height = round(img.shape[0]/2)
    width = round(img.shape[1]/2)

    color = img[height, width, :]

    print(color)
    return color

def detect_flag(img, color):

    
    blur = cv2.GaussianBlur(img, (9, 9), cv2.BORDER_DEFAULT)

    range = 30

    max = color.copy()
    min = color.copy()

    np.putmask(max, 255-range < max, 255-range)
    np.putmask(min, range > min, range )

    max += range
    min -= range
    print(max, min)

    

    mask = cv2.inRange(blur, min, max)
    
    edges = cv2.Canny(mask, 50, 150)
    edge = cv2.findNonZero(edges)
    # mid = (edge[:,0,0].max() + edge[:,0,0].min())/2
    mid = edge[:,0,0].mean()
    print(mid)
    


    plt.imshow(edges)
    plt.savefig('draw.png')




flag = cv2.imread('Flag.png')
cam = cv2.imread('CaptureTheFlag.png')

color = get_flag_color(flag)
detect_flag(cam, color)
