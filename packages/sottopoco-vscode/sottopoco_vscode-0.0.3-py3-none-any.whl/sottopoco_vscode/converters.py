import cv2
import numpy as np
import matplotlib.pyplot as plt
import os



def convert_matplotlib_to_opencv_img(matplotlib_format_img: object, clear=False, transitory_img_path='tmp_transition_image.jpg'):

    """
    It allows to convert a matplotlib image into a opencv one.

    matplotlib_format_img: It must be a matplotlib class object, like histograms from function cv2.calcHist.
    clear: If set to true, it will clear any existing matplotlib.pyplot object.
    transitory_img_path: It is just an unlikely filename for the temporary image wich will be created, so that it will not overwrite any file of the user in the working directory.
    """

    messages=[]

    # we can think of plt like an object which "hosts elements" which are "append-plotted" with the method plt.plot.
    # to clean the figure, plt.clf() must be used
    if clear:
        plt.clf()
        messages.append("- The element matplotlib.pyplot was reset ( matplotlib.pyplot.clf() was run )")

    if any(matplotlib_format_img):
        plt.plot(matplotlib_format_img)
        # otherwise it plots the already existing plt
        messages.append("- The input image was added to matplotlib.pyplot")
    else:
        raise IOError("No image was given in input!")

    try:
        plt.savefig(transitory_img_path)

        cv2_imread_format_img = cv2.imread(transitory_img_path)

        try: 
            os.remove(transitory_img_path)
        except: 
            raise OSError("Could not remove file {}".format(transitory_img_path))

    except: 
        raise OSError("Could not save img to {}".format(transitory_img_path))

    for m in messages:
        print(m)    

    return cv2_imread_format_img