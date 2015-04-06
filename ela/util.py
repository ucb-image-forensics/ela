from __future__ import absolute_import

import numpy as np

def rgb2gray(rgb):
    return np.dot(rgb[:, :, :3], [0.299, 0.587, 0.144])
