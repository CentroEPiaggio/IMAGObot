#!/usr/bin/python
import hal, time, serial

ser = serial.Serial("/dev/ttyACM0",115200,timeout=2)
time.sleep(1)

h = hal.component("arduino")
h.newpin("pressure", hal.HAL_FLOAT, hal.HAL_IN)
h.ready()

try:
    while 1:
        sig_extrude = h["pressure"]
        if int(sig_extrude) > 0:
            intPattern = '<'+str(sig_extrude)+'>'
            ser.write(intPattern.encode('utf-8'))
        elif int(sig_extrude) == 0:
            stopStr = 'a'
            ser.write(stopStr.encode('utf-8'))
            

except KeyboardInterrupt:
    raise SystemExit