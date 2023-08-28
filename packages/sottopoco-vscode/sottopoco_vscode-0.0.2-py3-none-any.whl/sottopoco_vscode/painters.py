import cv2
import numpy as np
import matplotlib.pyplot as plt
import os



def multiple_drawing(images: list, labels=[]):

    """
    It allows to display images on VScode.

    Press ESC to close all windows.

    images: list of images you want to display
    labels: list of the labels of the images   

    """

    if not images:
        raise IOError("No image was given in input!")
    
    if not isinstance(images, list):
        raise TypeError("The first argument must be a list. You gave me {}, which is {}".format(images, type(images)))


    print("--- multiple_drawing --- S")

    # print("images: {}".format(images))

    # labeling
    if not labels:

        labels = []
        for idx, image in enumerate(images):
            labels.append( "my_drawing_" + str(idx+1))
            # only here I make the human friendly index

        # labels = [ "my_drawing_" + str(index()) for image in images ]

    else:

        if not isinstance(labels, list):
            raise TypeError("The second argument must be a list. You gave me {}, which is {}".format(labels, type(labels)))

        if len(labels) < len(images):
            raise IndexError(
                "There are not as many labels ({}) as the input images ({})!".format(
                len(labels) , len(images))
                )

    for idx, image in enumerate(images):
        cv2.namedWindow(winname=labels[idx])
        # print( 'my_drawing_'+str(idx) )

    for idx, image in enumerate(images):
        cv2.imshow(labels[idx], image)

    while True:
        if cv2.waitKey(1) & 0xFF == 27: # press esc
            break

    cv2.destroyAllWindows()

    print("--- multiple_drawing --- E")



#---------------------------------------------------------------------------------------



def cyclical_drawing(images: list, labels=[]):

    """
    It allows to display images and videos we want to draw on in real time, on VScode.

    Press ESC to close all windows.

    images: list of images you want to display
    labels: list of the labels of the images

    (!) WARNING \n    This function might be very CPU and RAM consuming.    
    """

    print("--- cyclical drawing --- S")

    if not images:
        raise IOError("No image was given in input!")
    
    if not isinstance(images, list):
        raise TypeError("The first argument must be a list. You gave me {}, which is {}".format(images, type(images)))

    # print("images: {}".format(images))

    # main
    #-------

    # labeling
    if not labels:

        labels = []
        for idx, image in enumerate(images):
            labels.append( "my_drawing_" + str(idx+1))
            # only here I make the human friendly index

        # labels = [ "my_drawing_" + str(index()) for image in images ]

    else:

        if not isinstance(labels, list):
            raise TypeError("The second argument must be a list. You gave me {}, which is {}".format(labels, type(labels)))

        if len(labels) < len(images):
            raise IndexError(
                "There are not as many labels ({}) as the input images ({})!".format(
                len(labels) , len(images))
                )

    for idx, image in enumerate(images):
        cv2.namedWindow(winname=labels[idx])
        # print( 'my_drawing_'+str(idx) )

    while True:
        for idx, image in enumerate(images):
            cv2.imshow(labels[idx], image)

        if cv2.waitKey(1) & 0xFF == 27: # press esc
            break

    cv2.destroyAllWindows()

    print("--- cyclical drawing --- E")