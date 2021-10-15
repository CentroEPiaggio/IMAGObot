#!/usr/bin/env python
import hal
import time
import serial
import linuxcnc

s = linuxcnc.stat()

ser = serial.Serial("/dev/ttyACM0", 9600)

rs = hal.component("relay")
rs.newpin("state", hal.HAL_BIT, hal.HAL_IN)
rs.ready()

try:
 while 1:
        s.poll()
        status = rs['state']
        if status == True:
            ser.write(b'H')
        elif status == False:
            ser.write(b'L')

except KeyboardInterrupt:
    raise SystemExit