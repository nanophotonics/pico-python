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
                               'waveform_duration',
                               'sampling_interval', 
                               'number_of_samples',
                               'trigger_channel',
                               'trigger_threshold',
                               'trigger_direction',
                               )
    def __init__(self):
        print("Attempting to open Picoscope 5000a...\n")
        
        ps5000a.PS5000a.__init__(self)
        Instrument.__init__(self)
        
        print("Found the following picoscope:\n")
        print(self.getAllUnitInfo() + '\n')
#        print('')
        
        self._model_name = None
        self._serial_number = None
        self._integration_time = None
        self._channels = None
        self._waveform_duration = None
        self._sampling_interval = None
        self._number_of_samples = None
        self._trigger_channel = None
        self._trigger_threshold = None
        self._trigger_direction = None
        
        self._waveform_duration = 150.0E-6 # seconds
#        self._number_of_samples = 4096
        self._sampling_interval = 8.0E-9 # seconds
        self.calculate_number_of_samples()
#        self.calculate_sampling_interval()
        
        
    def calculate_sampling_interval(self):
        try:
            self._sampling_interval = self._waveform_duration / self._number_of_samples
            return self._sampling_interval
        except:
            return print('Set waveform_duration and number_of_samples before',
                         'trying to calculate the sampling_interval.\n')
            
    def get_sampling_interval(self):
        if self._sampling_interval is None:
            self.calculate_sampling_interval()
        return self._sampling_interval
    sampling_interval = property(get_sampling_interval)
    
    def set_sampling_interval(self):
        try:
            self.calculate_sampling_interval() # recalculate the sampling interval first
            (self._sampling_interval, self._number_of_samples, self.max_samples) = \
                self.setSamplingInterval(self._sampling_interval, self._waveform_duration)
            print("Waveform duration = %f ms" % (self._waveform_duration * 1E6))
            print("Sampling interval = %f ns" % (self._sampling_interval * 1E9))
            print("Taking  samples = %d" % self._number_of_samples)
            print("Maximum samples = %d" % self.max_samples)
        except:
            print('Unable to set the sampling interval.\n')
    
    def calculate_number_of_samples(self):
        try:
            self._number_of_samples = round(self._waveform_duration / self._sampling_interval)
            return self._number_of_samples
        except:
            return print('Set waveform_duration and sampling_interval before'
                         'trying to calculate the number_of_samples.\n')   
                         
    def get_number_of_samples(self):
        if self._number_of_samples is None:
            self.calculate_number_of_samples()
        return self._number_of_samples
    number_of_samples = property(get_number_of_samples)
    
    def calculate_waveform_duration(self):
        try:
            self._waveform_duration = self._number_of_samples * self._sampling_interval
            return self._waveform_duration
        except:
            return print('Set number_of_samples and sampling_interval before'
                         'trying to calculate the waveform_duration.\n')            
    def get_waveform_duration(self):
        if self._waveform_duration is None:
            self.calculate_waveform_duration()
        return self._waveform_duration
    waveform_duration = property(get_waveform_duration)
    
    def get_model_name(self):
        if self._model_name is None:
            self._model_name = self.getUnitInfo('VarianInfo')
        return self._model_name
    model_name = property(get_model_name)
    
    def get_serial_number(self):
        if self._serial_number is None:
            self._serial_number = self.getUnitInfo('BatchAndSerial')
        return self._serial_number
    serial_number = property(get_serial_number)


if __name__ == "__main__":
    print(__doc__)
    
    ps = PicoScope5000a()
    
#    print("Found the following picoscope:")
#    print(ps.getAllUnitInfo())
    
    ps.model_name
    ps.serial_number
    
    ps.set_sampling_interval()
    

    
#    ps.show_gui()