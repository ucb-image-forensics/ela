from __future__ import absolute_import

from .ela import ELA
from .metrics import BasicMetricsELA
from .util import iterate_with_progress

import numpy as np
import scipy.io as sio

import sys, os


def main():
    directory = sys.argv[1]

    for filename in iterate_with_progress(os.listdir(directory)):
        ela = ELA(directory + '/' + filename)
        metrics = BasicMetricsELA(ela)
        raw_basic_metrics = np.array(metrics.metrics)
        aggregate_metrics = np.array([metrics.aggregate_mean, metrics.aggregate_variance])

if __name__ == '__main__':
    main()
