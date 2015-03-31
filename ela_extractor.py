#!/usr/bin/env python
import numpy as np
from PIL import Image, ImageChops, ImageEnhance
from scipy import ndimage

def rgb2gray(rgb):
    return np.dot(rgb[:, :, :3], [0.299, 0.587, 0.144])

class ELA(object):
    """
    ELA object that represents the error level of a given image.

    Error Level Analysis (ELA) is a method of quantifying the JPEG
    compression loss on a per pixel basis.
    """

    def __init__(self, filename, resave_quality=95):
        self.resave_quality = resave_quality
        self.filename = filename
        self._resave_first_image()
        self.filtered_image = None
        self.run_ela()

    @property
    def data(self):
        return self.ela_image_data

    @property
    def data_one_channel(self):
        return np.sqrt(
            self.ela_image_data[:, :, 0]**2
            + self.ela_image_data[:, :, 1]**2
            + self.ela_image_data[:, :, 2]**2
        )

    @property
    def mask(self):
        im = ndimage.imread(self.filename)
        mask = ndimage.filters.gaussian_filter(rgb2gray(self.ela_image_data), 5, order=1)
        return mask #1 / (mask + 1)

    @property
    def combined_filter_one_channel(self):
        return 50 * (rgb2gray(self.ela_image_data) ** 2) * self.mask

    @property
    def combined_filter(self):
        if self.filtered_image == None:
            self.filtered_image = np.zeros(self.ela_image_data.shape)
            self.filtered_image[:,:,0] = self.ela_image_data[:,:,0] * (self.mask ** 2)
            self.filtered_image[:,:,1] = self.ela_image_data[:,:,1] * (self.mask ** 2)
            self.filtered_image[:,:,2] = self.ela_image_data[:,:,2] * (self.mask ** 2)
        return self.filtered_image

    @property
    def combined_filter_scaled(self):
        scale = 255.0/np.max(self.combined_filter)*0.8
        return self.combined_filter * scale

    def show_ela_image(self, re_scale=True):
        if re_scale:
            extrema = self.ela_image.getextrema()
            max_diff = max([ex[1] for ex in extrema])
            scale = 255.0/(max_diff*0.8)
            ImageEnhance.Brightness(self.ela_image).enhance(scale).show()
        else:
            self.ela_image.show()

    def run_ela(self):
        self._resave_image()
        self.ela_image = ImageChops.difference(self.image, self.resaved_image)
        self.ela_image_data = np.array(self.ela_image)
        return self.ela_image_data

    def _resave_image(self):
        resaved = self.filename + '.resaved.jpg'
        self.image.save(resaved, 'JPEG', quality=self.resave_quality)
        self.resaved_image = Image.open(resaved)

    def _resave_first_image(self):
        resaved = self.filename + '.r1.jpg'
        Image.open(self.filename).save(
            resaved, 'JPEG', quality=100)
        self.image = Image.open(resaved)

class FilteredMetricsELA(object):

    def __init__(self, ela):
        self.ela_fitlered_data = ela.combined_filter_one_channel
        self.generate_metrics()

    def generate_metrics(self):
        mean = np.mean(self.ela_fitlered_data)
        median = np.median(self.ela_fitlered_data)
        var = np.var(self.ela_fitlered_data)
        max_v = np.max(self.ela_fitlered_data)

        self.metrics = (mean, median, var, max_v)

    @property
    def variance(self):
        return self.metrics[2]

    @property
    def mean(self):
        return self.metrics[0]

    @property
    def max_v(self):
        return self.metrics[max_v]

class BasicMetricsELA(object):

    def __init__(self, ela):
        self.ela_image_data = ela.data
        self.generate_metrics()

    def generate_metrics(self):
        ela_image_data_r = self.ela_image_data[:, :, 0]
        r_mean = np.mean(ela_image_data_r)
        r_median = np.median(ela_image_data_r)
        r_var = np.var(ela_image_data_r)

        ela_image_data_g = self.ela_image_data[:, :, 1]
        g_mean = np.mean(ela_image_data_g)
        g_median = np.median(ela_image_data_g)
        g_var = np.var(ela_image_data_g)

        ela_image_data_b = self.ela_image_data[:, :, 2]
        b_mean = np.mean(ela_image_data_b)
        b_median = np.median(ela_image_data_b)
        b_var = np.var(ela_image_data_b)

        self.metrics = (
            r_mean, r_median, r_var,
            g_mean, g_median, g_var,
            b_mean, b_median, b_var,
        )

    @property
    def aggregate_variance(self):
        return (
            self.metrics[2] + self.metrics[5] + self.metrics[8]
        )

    @property
    def aggregate_mean(self):
        return (
            self.metrics[0] + self.metrics[3] + self.metrics[6]
        )
