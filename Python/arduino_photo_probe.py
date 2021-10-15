#!/usr/bin/env python

import serial
import hal
import linuxcnc

s = linuxcnc.stat()

PORT = "/dev/ttyACM0"
ser = serial.Serial(PORT,9600)

photo = hal.component("photoresistor")
photo.newpin("out",hal.HAL_S32,hal.HAL_OUT)
photo.ready()

outFileName= "joint_angles_photo.txt"
file = open(outFileName,"w")

outFileName_2= "joint_angles_probe_photo.txt"
file_2 = open(outFileName_2,"w")

state = 1

try:
 while 1:
  while ser.inWaiting():

    s.poll()
    val = ord(ser.read())
    photo['out'] = val
    
    threshold  = s.ain[0]

    if state != 0:

      if s.probe_val == 0:

        if (state == 1):
         old_val = val
         state = 2
    
        elif(state == 2):
 
         #if (old_val - val)> threshold:
	 	
         if val < threshold:   

           state = 3

           x = s.joint_actual_position[0]
           y = s.joint_actual_position[1]
           z = s.joint_actual_position[2]
           a = s.joint_actual_position[3]
           b = s.joint_actual_position[4]
        
           with open(outFileName,"a") as file:
            file.write("X"+str(x)+" Y"+str(y)+" Z"+str(z)+" A"+str(a)+" B"+str(b)+'\n')
           
           

      elif (s.probe_val == 1 and state == 3): 
          
          state = 0
          
          x = s.joint_actual_position[0]
          y = s.joint_actual_position[1]
          z = s.joint_actual_position[2]
          a = s.joint_actual_position[3]
          b = s.joint_actual_position[4]
        
          with open(outFileName_2,"a") as file_2:
           file_2.write("X"+str(x)+" Y"+str(y)+" Z"+str(z)+" A"+str(a)+" B"+str(b)+'\n')
          
          

        
    if s.probing == 0:

      state = 1


except KeyboardInterrupt:
 raise SystemExit

