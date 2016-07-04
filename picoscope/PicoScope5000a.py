# -*- coding: utf-8 -*-
"""
Created on Mon Jul 04 14:20:20 2016

@author: Ana Andres
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from picoscope import ps5000a
from nplab.instrument import Instrument
import time
import pylab as plt
import numpy as np



class PicoScope5000a(ps5000a.PS5000a, Instrument):
    """
    Class representing the PicoScope, via the pico-python
    """
    metadata_property_names = ('model_name',
                               'serial_number', 
                               'integration_time',
                               'channels', 
                               'sampling_interval', 
                               'number_of_samples',
                               'trigger_channel',
                               'trigger_threshold',
                               'trigger_direction',
                               )
    def __init__(self):
        ps5000a.PS5000a.__init__(self)
        Instrument.__init__(self)


if __name__ == "__main__":
    print(__doc__)
    print("Attempting to open Picoscope 5000a...")
    
    ps = PicoScope5000a()
    
    print("Found the following picoscope:")
    print(ps.getAllUnitInfo())
    
#    ps.show_gui()