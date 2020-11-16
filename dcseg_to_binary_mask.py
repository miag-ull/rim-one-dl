import numpy as np
from scipy.signal import resample_poly
from skimage.draw import polygon2mask
from skimage.io import imread


def dcseg_to_binary_mask(img_filename, dcseg_filename):
    """Convert a mask in DCSeg TXT format to a binary mask.

    :param img_filename: full path to the image file to generate the binary mask for (string)
    :param dcseg_filename: full path to the DCSeg TXT mask file to be converted to a binary mask (string)
    :return: NumPy 2D boolean array with the binary mask generated from the given DCSeg TXT mask for the given image.
    """
    img = imread(img_filename)
    dcseg_file = open(dcseg_filename, 'r')
    lines = dcseg_file.readlines()

    # First line can be discarded, it's just informative (line 0)
    # Second and third lines are the coordinates of the center (lines 1 and 2). Can also be ignored.
    # Read the 16 points of the contour selected by the user and transform to int (lines 3 to 35)
    points_x = []
    points_y = []
    for i in range(3, 35, 2):
        points_x.append(int(lines[i]) - 1)
        points_y.append(int(lines[i+1]) - 1)

    # Repeat the initial point at the end to interpolate from the last one (close the polygon)
    points_x.append(points_x[0] - 1)
    points_y.append(points_y[0] - 1)

    padtype = 'antireflect'
    interp_x1 = resample_poly(points_x, 50, 1, padtype=padtype)
    interp_y1 = resample_poly(points_y, 50, 1, padtype=padtype)

    points = []
    for i in range(0, 16*50-1):
        # Invert X and Y (points have to be in [row, col] format)
        points.append([interp_y1[i], interp_x1[i]])

    mask = polygon2mask((img.shape[0], img.shape[1]), np.array(points))

    return mask
