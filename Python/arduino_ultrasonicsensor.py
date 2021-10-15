#!/usr/bin/env python

import serial
import hal
import linuxcnc
import time
import math


s = linuxcnc.stat()

PORT = "/dev/ttyACM1"
ser = serial.Serial(PORT,9600)

sensor = hal.component("distance")
sensor.newpin("value",hal.HAL_FLOAT,hal.HAL_OUT)
sensor.ready()

outFileName= "joint_angles_height.txt"
file = open(outFileName,"w")

state = 1



try:

 while 1:

  while ser.inWaiting():
    
    
  
    s.poll()
    val = ord(ser.read())
    sensor['value'] = val

    if s.exec_state == 8:  # DELAY STATE
    
      if state == 1:

          pause_time = math.ceil(s.delay_left)
          time.sleep(pause_time/2)

          height = val*4

          x = s.actual_position[0]
          y = s.actual_position[1]
          z = s.actual_position[2]
          a = s.actual_position[3]
          b = s.actual_position[4]

          with open(outFileName,"a") as file:
            file.write("X"+str(x)+" Y"+str(y)+" Z"+str(z)+" A"+str(a)+" B"+str(b)+" H"+str(height)+'\n')
       
          state = 0

    else:

     state = 1


except KeyboardInterrupt:
 raise SystemExit

