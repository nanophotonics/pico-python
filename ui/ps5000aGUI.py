"""
PS5444B Test.
By: Ana Andres-Arroyo
"""

import picoscope
import matplotlib.pyplot as plt
import numpy as np
import time
from ctypes import *

picoscope = reload(picoscope)
from picoscope import ps5000a
ps5000a = reload(ps5000a)

from nplab.ui.ui_tools import UiTools

class PicoScopeGUI(QtGui.QMainWindow, UiTools):
    """
    GUI which records data from the PicoScope.
    """
    
    def __init__(self, data_file, parent=None):
        super(HDF5SpectrumAnalyser, self).__init__(parent)
        self.data_file = data_file
        uic.loadUi(os.path.join(os.path.dirname(__file__), 'PicoScopeGUI.ui'), self)
        
        self.setChannels_pushButton.clicked.connect(self.set_channels)
    
    def set_channels(self):
        pass

if __name__ == "__main__":
    print(__doc__)

    print("Attempting to open Picoscope 5000a...")

#    SERIAL_NUM = 'CS960/049'
#    ps = ps5000a.PS5000a(SERIAL_NUM) # specity the serial number
    ps = ps5000a.PS5000a() # automatically detect the serial number 
    
    print("\nFound the following picoscope:")
    print(ps.getAllUnitInfo() + "\n")
    

    
    """
    Set up a specific channel.

    It finds the smallest range that is capable of accepting your signal.
    Return actual range of the scope as double.

    The VOffset, is an offset that the scope will ADD to your signal.

    If using a probe (or a sense resitor), the probeAttenuation value is used 
    to find the approriate channel range on the scope to use.

    e.g. to use a 10x attenuation probe, you must supply the following 
    parameters ps.setChannel('A', "DC", 20.0, 5.0, True, False, 10.0)

    The scope will then be set to use the +- 2V mode at the scope allowing you 
    to measure your signal from -25V to +15V.
    After this point, you can set everything in terms of units as seen at the 
    tip of the probe. For example, you can set a trigger of 15V and it will 
    trigger at the correct value.

    When using a sense resistor, lets say R = 1.3 ohm, you obtain the relation:
    V = IR, meaning that your probe as an attenuation of R compared to the 
    current you are trying to measure.

    You should supply probeAttenuation = 1.3
    The rest of your units should be specified in amps.

    Unfortunately, you still have to supply a VRange that is very close to the 
    allowed values. This will change in furture version where we will find the 
    next largest range to accomodate the desired range.

    If you want to use units of mA, supply a probe attenuation of 1.3E3.
    Note, the authors recommend sticking to SI units because it makes it easier 
    to guess what units each parameter is in.

    """
    channelRangeA = ps.setChannel(channel="A",                                  
                                 coupling="DC", 
                                 VRange=10.0, 
                                 VOffset=0.0,
                                 enabled=True,                                  
                                 BWLimited=False,
                                 probeAttenuation=1.0,
                                 )
    print("A channel range = %d V" % channelRangeA)
    
    channelRangeB = ps.setChannel(channel="B",                                  
                                 coupling="DC", 
                                 VRange=10.0, 
                                 VOffset=0.0,
                                 enabled=True,                                  
                                 BWLimited=False,
                                 probeAttenuation=1.0,
                                 )
    print("B channel range = %d V" % channelRangeA)
    
    """
    Sampling interval and timebase setup.
    """
    waveform_duration = 600E-3 # seconds
    number_of_samples = 4096
    sampling_interval = waveform_duration / number_of_samples

    (actualSamplingInterval, nSamples, maxSamples) = \
        ps.setSamplingInterval(sampling_interval, waveform_duration)
    print("Sampling interval = %f ns" % (actualSamplingInterval * 1E9))
    print("Taking  samples = %d" % nSamples)
    print("Maximum samples = %d" % maxSamples)

    """
    Simple Trigger setup.

    trigSrc can be either a number corresponding to the low level
    specifications of the scope or a string such as 'A' or 'AUX'

    direction can be a text string such as "Rising" or "Falling",
    or the value of the dict from self.THRESHOLD_TYPE[] corresponding
    to your trigger type.

    delay is number of clock cycles to wait from trigger conditions met
    until we actually trigger capture.

    timeout_ms is time to wait in mS from calling runBlock() or similar
    (e.g. when trigger arms) for the trigger to occur. If no trigger
    occurs it gives up & auto-triggers.

    Support for offset is currently untested

    Note, the AUX port (or EXT) only has a range of +- 1V (at least in PS6000)
    """
    ps.setSimpleTrigger(trigSrc='A', 
                        threshold_V=0.5, 
                        direction='Rising', 
                        delay=0,
                        timeout_ms=100, 
                        enabled=True
                        )


    """
    Block mode setup. 
    
    In block mode, the computer prompts a PicoScope 5000 Series oscilloscope to 
    collect a block of data into its internal memory. When the oscilloscope has 
    collected the whole block, it signals that it is ready and then transfers 
    the whole block to the computer's memory through the USB port.
    """    
    
    """
    Rapid block mode setup. 
    
    Rapid block mode allows you to sample several waveforms at a time with the
    minimum time between waveforms. It reduces the gap from milliseconds to 
    less than 2 microseconds (on fastest timebase).
    """ 

    """
    This function sets the number of captures to be collected in one run of 
    rapid block mode. If you do not call this function before a run, the driver 
    will capture only one waveform. Once a value has been set, the value 
    remains constant unless changed.
    """    
    number_of_captures = 1
    ps.setNoOfCaptures(number_of_captures)
    
    """
    Streaming mode setup.
    
    Streaming mode can capture data without the gaps that occur between blocks 
    when using block mode. Streaming mode supports downsampling and triggering, 
    while providing fast streaming at up to 31.25 MS/s (32 ns per sample) when 
    one channel is active, depending on the computer's performance. This makes 
    it suitable for high-speed data acquisition, allowing you to capture long 
    data sets limited only by the computer's memory.
    
    TO DO! The low level functions in ps5000a.py are mostly empty
    """
    
    ps.runBlock()
    ps.waitReady()
    (dataA, numSamplesReturnedA, overflowA) = ps.getDataRaw(channel='A', 
                                                         numSamples=0, 
                                                         startIndex=0, 
                                                         downSampleRatio=1,
                                                         downSampleMode=0, 
                                                         segmentIndex=0, 
                                                         data=None,
                                                         )
                                                         
    (dataB, numSamplesReturnedB, overflowB) = ps.getDataRaw(channel='B', 
                                                         numSamples=0, 
                                                         startIndex=0, 
                                                         downSampleRatio=1,
                                                         downSampleMode=0, 
                                                         segmentIndex=0, 
                                                         data=None,
                                                         )
    
    plt.plot(dataA)
    plt.plot(dataB)

#    
#    c = 3e8
#   
#    # rapid block mode
#    
#    ps.setChannel(channel="A", coupling="DC", VRange=1)
#    
#    n_captures = 2300 * 3 #int(600 * 1.4)
#    sample_interval = 5 / 3e8
#    sample_duration = 1e3 * 2 / 3e8
#    
#    ps.setSamplingInterval(sample_interval, sample_duration)
#    ps.setSimpleTrigger("A", threshold_V=0.2)
#    
#    samples_per_segment = ps.memorySegments(n_captures)
#    ps.setNoOfCaptures(n_captures)
#    
#    data = np.zeros((n_captures, samples_per_segment), 
#    	dtype=np.int16)
#    
#    t1 = time.time()
#    
#    ps.runBlock()
#    ps.waitReady()
    
#    t2 = time.time()
#    print "Time to get sweep: ", str(t2 - t1)
#    
#    
#    
#    ps.getDataRaw(data=data)
#    
#    
#    
#    
#    
#    # for i in range(n_captures): 
#    # 	ps._lowLevelSetDataBuffer(ps.CHANNELS["A"],
#    # 		data[i, :], 0, i)
#    
#    # # t2 = time.time()
#    # nsamples = c_int32(ps.noSamples)
#    # from_segment_index = 0
#    # to_segment_index = n_captures - 1
#    # downsample_ratio = 0
#    # downsample_mode = 0
#    # overflow = np.zeros(n_captures, dtype=np.int16)
#    # overflow_ptr = overflow.ctypes.data_as(POINTER(c_int16))
#    
#    # m = ps.lib.ps5000aGetValuesBulk(c_int16(ps.handle),
#    # 		byref(nsamples),
#    # 		c_int16(from_segment_index),
#    # 		c_int16(to_segment_index),
#    # 		c_int32(downsample_ratio),
#    # 		c_int16(downsample_mode),
#    # 		overflow_ptr)
#    # print m
#    
#    # ps.checkResult(m)
#    
#    t3 = time.time()
#    print "Time to read data: ", str(t3 - t2)
#    
#    
#    # output_file.write(data)
#    # t4 = time.time()
#    # print "Time to write data to disk: ", str(t4 - t3)
#    # output_file.close()
#    
#    plt.imshow(data[:, 0:ps.noSamples], aspect='auto', interpolation='none',
#    	cmap=plt.cm.hot)
#    plt.colorbar()
#    plt.show()
    
    ps.close()