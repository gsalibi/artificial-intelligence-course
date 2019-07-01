import numpy as np
import cv2
import matplotlib.pyplot as plt
import sys

def ImagePlot(img,title=None):
    plt.imshow(img)
    plt.axis('off')
    plt.title(title)
    plt.show()
    
def SaveImg(img,path):
    cv2.imwrite(path,img)

img = cv2.imread(sys.argv[1])

mean = 0
var = 4000
sigma = var ** 0.5
gaussian = np.random.normal(mean, sigma, (img.shape)) 

noisy_image = img + gaussian

cv2.normalize(noisy_image, noisy_image, 0, 255, cv2.NORM_MINMAX, dtype=-1)
noisy_image = noisy_image.astype(np.uint8)

SaveImg(noisy_image,sys.argv[2])
