from __future__ import absolute_import

from ela import ELA
from ela.metrics import BasicMetricsELA

import sys, os

def main():
    directory = sys.argv[1]

    for filename in os.listdir(directory):
        ela = ELA(directory + '/' + filename)
        ela_metrics = BasicMetricsELA(ela)
        print filename
        print ela_metrics.metrics

if __name__ == '__main__':
    main()
