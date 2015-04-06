#!/usr/bin/env python

from __future__ import absolute_import

from ela_extractor import *
import sys, os

directory = sys.argv[1]

for filename in os.listdir(directory):
    ela = ELA(directory + '/' + filename)
    ela_metrics = BasicMetricsELA(ela)
    import pdb; pdb.set_trace();
    print filename
    print ela_metrics.metrics
