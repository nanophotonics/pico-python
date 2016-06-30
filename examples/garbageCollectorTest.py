"""
Test the garbage collection if we pass the picoscope object.

By: Mark Harfouche

"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from picoscope import ps5000a

# import the garbage collection interface
import gc

if __name__ == "__main__":
    ps = ps5000a.PS5000a()

    print("Found the following picoscope:")
    print("Serial: " + ps.getUnitInfo("BatchAndSerial"))

    pd = ps

    print("Copied the picoscope object, the information of the copied object is:")
    print("Serial: " + pd.getUnitInfo("BatchAndSerial"))

    print("\n\n\n")

    print("Using both objects")
    ps.setChannel('A')
    pd.setChannel('B')

    del ps

    print("Deleting the original object and collecting garbage.")

    gc.collect()
    print("Copied object still works:")
    print("Serial: " + pd.getUnitInfo("BatchAndSerial"))

    pd.close()
    print("Now I closed the other object.")
