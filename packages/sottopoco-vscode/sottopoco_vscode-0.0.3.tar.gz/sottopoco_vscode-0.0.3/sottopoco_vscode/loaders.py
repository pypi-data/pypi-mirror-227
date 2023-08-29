import cv2
import numpy as np
import matplotlib.pyplot as plt
import os



def load_img(path: str, resize=0.0, recolor=False, greyscale=False):

    """
    It allows to load an image from a path and immediatly apply it some transformations.

    path: The path of the image you want to load.
    resize: It allows to directly resize the image you want to load ( e.g. resize=1.5 -> 150% ). \n        The same resize will be applied to both vertical and horizontal dimensions.
    recolor: It allows to directly recolor the image you want to load. \n        It must be like cv2.COLOR_BGR2RGB , cv2.COLOR_BGR22GRAY, cv2.COLOR_BGR2HSV , ecc.
    greyscale: It allows to directly greyscale recolor the image you want to load. 
    """

    messages=[]

    if not os.path.exists(path):
        raise IOError("File {} does not exist!".format(path))

    if greyscale:
        img1 = cv2.imread(path, 0)
        messages.append("- Greyscale recoloring applied")
    else:
        img1 = cv2.imread(path)

    if resize > 0:
        factor = resize
        img1 = cv2.resize(img1, (0,0), fx=factor, fy=factor) 
        messages.append("- Resize factor applied: {}".format(factor))

    if recolor:
        # cv2.COLOR_BGR2RGB
        img1 = cv2.cvtColor(img1, recolor)
        messages.append("- Color conversion applied: {}".format(str(recolor)))

        
    print("A new image was loaded: {}".format(path))

    for m in messages:
        print(m)

    return img1