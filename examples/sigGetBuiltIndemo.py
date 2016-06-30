"""
PS5000a Siggen Demo.

By: Mark Harfouche

This is a demo of how to use Siggen with the Picoscope 5000a
UNTESTED. NO: It was tested with the PS5444B USB2.0 version

The system is very simple:

The SigGen is connected to Channel A. No other setup is required

Warning, the picoscope has a bug, that doesn't let you generate a waveform correctly for a while
It means that you need to kick it in place

See http://www.picotech.com/support/topic12969.html

"""
from __future__ import division

import time
from picoscope import ps5000a
import pylab as plt
import numpy as np

if __name__ == "__main__":
    print(__doc__)

    print("Attempting to open Picoscope 5000a...")

    # see page 13 of the manual to understand how to work this beast
    ps = ps5000a.PS5000a()

    print(ps.getAllUnitInfo())

    waveform_desired_duration = 1E-3
    obs_duration = 10 * waveform_desired_duration
    sampling_interval = obs_duration / 4096

    (actualSamplingInterval, nSamples, maxSamples) = ps.setSamplingInterval(sampling_interval,
                                                                            obs_duration)
    print("Sampling interval = %f ns" % (actualSamplingInterval * 1E9))
    print("Taking  samples = %d" % nSamples)
    print("Maximum samples = %d" % maxSamples)

    ps.setChannel('A', 'DC', 5.0, 0.0, True, False)
    ps.setSimpleTrigger('A', 0.0, 'Rising', delay=0, timeout_ms=100, enabled=True)

    ps.setSigGenBuiltInSimple(offsetVoltage=0, pkToPk=4, waveType="Square",
                              frequency=1 / waveform_desired_duration * 10, shots=1,
                              triggerType="Rising", triggerSource="None")

    # take the desired waveform
    # This measures all the channels that have been enabled

    ps.runBlock()
    ps.waitReady()
    print("Done waiting for trigger")
    time.sleep(10)
    ps.runBlock()
    ps.waitReady()

    dataA = ps.getDataV('A', nSamples, returnOverflow=False)

    ps.stop()
    ps.close()

    dataTimeAxis = np.arange(nSamples) * actualSamplingInterval

    plt.ion()

    plt.figure()
    plt.hold(True)
    plt.plot(dataTimeAxis, dataA, label="Waveform")
    plt.grid(True, which='major')
    plt.title("Picoscope 5000a waveforms")
    plt.ylabel("Voltage (V)")
    plt.xlabel("Time (ms)")
    plt.legend()
    plt.draw()
