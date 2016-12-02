"""
PS5444B Test.
By: Ana Andres-Arroyo
"""

#import picoscope
import matplotlib.pyplot as plt
import numpy as np
import time
from ctypes import *

#picoscope = reload(picoscope)
#from picoscope import ps5000a
#ps5000a = reload(ps5000a)
from picoscope import PicoScope5000a

if __name__ == "__main__":
    print(__doc__)
    
    """Instantiate the picoscope object"""
    ps = PicoScope5000a.PicoScope5000a()
    
    """Specify which channels to use."""
    ps_channels = ['A', 'B']
#    ps_channels = ['B']    
    
    """Sampling interval and timebase setup."""    
    waveform_duration = 1.5 # seconds
    number_of_samples = 2**11
    sampling_interval = waveform_duration / number_of_samples
    (actualSamplingInterval, nSamples, maxSamples) = \
        ps.setSamplingInterval(sampling_interval, waveform_duration)
        
    print("Waveform duration = %f s" % (nSamples * actualSamplingInterval))
    print("Sampling interval = %f ns" % (actualSamplingInterval * 1E9))
    print("Taking  samples = %d" % nSamples)
    print("Maximum samples = %d" % maxSamples)
    print('\n')

    """Simple Trigger setup."""
    ps.setSimpleTrigger(trigSrc=ps_channels[0], 
                        threshold_V=0.02, 
                        direction='Rising', 
                        delay=0,
                        timeout_ms=100, 
                        enabled=True
                        )

  
    """Rapid block mode setup."""   
    number_of_captures = 1
    ps.setNoOfCaptures(number_of_captures)    
    
    
    ps_channels_range = []
    ps_data = []                                                         
    for i in range(len(ps_channels)):
        ps_channels_range.append(0.02)
        ps_data.append([])
        
        data = [0.0, 0.0] 
        channelRange = ps_channels_range[i]            
        while max(data) < ps_channels_range[i]*0.3 or \
              max(data) > ps_channels_range[i]*0.95:
                        
            """Set up channel range."""
            channelRange = ps.setChannel(channel=ps_channels[i],
                                 coupling="DC", 
                                 VRange=channelRange, 
                                 VOffset=0.0,
                                 enabled=True,                                  
                                 BWLimited=False,
                                 probeAttenuation=1.0,
                                 ) 
            print 'Channel ' + ps_channels[i] + ' range = ' + str(channelRange) + ' V'
            ps_channels_range[i] = channelRange
    
            """Collect data."""
            ps.runBlock()
            ps.waitReady()
                  
            """Read data from the buffer."""
            (data, numSamplesReturned, overflow) = \
                ps.getDataRaw(channel=ps_channels[i])
                
            """Convert data to volts."""
            data = data/32512.0*ps_channels_range[i]
            print 'Maximum voltage = ' + str(max(data)) + ' V\n'
            
            """Modify chanel range if data is too small/big."""
            if max(abs(data)) < ps_channels_range[i]*0.3:
                channelRange = channelRange / 2.5
            elif max(abs(data)) > ps_channels_range[i]*0.95:
                channelRange = channelRange * 2              
            elif max(abs(data)) >= 12:
                print 'WARNING!!! Channel ' + ps_channels[i] + ' is saturated!!!'
                
            if channelRange < 0.005 or channelRange > 20.0:
                print 'Exit PicoScope autorange loop\n'
                break          
        
        
        """Append data to list."""
        ps_data[i].append(data)
        
        """Plot data."""
        plt.plot(data)
        
    ps.close()

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
    
    