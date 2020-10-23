#!/usr/bin/python
#
#    Copyright Marco Antoni, Michele Scorsipa 2017
#    Copyright Chew-Z 2017
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# Graphic model of a IMAGObot 3D Printed robot arm
#
#  - Unit are in mm !
#  - Link7 is dummy link , IMAGObot has 5DOF
#
#
#             L3
#    j2  *----------*   j3
#        |       L4 | 
#    L2  |          *   j4
#        |       L5 |
#    j1  *          *   j5
#        |       L6 |
#    L1  |          *   j6
#                L7 |
#                  | |  end-effector
#                                   
#     

from vismach import *
import hal

## Config Vars
debug_orig_axis = True    # Enable orig (0,0,0) cross reference
debug_orig_effector = True  # Enable cross reference to end effector
# Add an offset to end effector (mm)
toolZ_offset = 60 - 17.491
# Models colors
default_color = [0.5,0.5,0.5,1]
tooltip_color = [0.5,0.5,0.5,1]
tip_color = [1,1,1,0]
base_color = [0.18,0.19,0.2,1]
floor_color = [1,1,1,1] 
refx_color = [0,1,0,1]
refy_color = [1,0,0,1]
refz_color = [0,0,1,1]

## HAL Pins
c = hal.component("IMAGObotgui")
c.newpin("joint1", hal.HAL_FLOAT, hal.HAL_IN)
c.newpin("joint2", hal.HAL_FLOAT, hal.HAL_IN)
c.newpin("joint3", hal.HAL_FLOAT, hal.HAL_IN)
c.newpin("joint4", hal.HAL_FLOAT, hal.HAL_IN)
c.newpin("joint5", hal.HAL_FLOAT, hal.HAL_IN)
c.newpin("joint6", hal.HAL_FLOAT, hal.HAL_IN)
c.newpin("grip", hal.HAL_FLOAT, hal.HAL_IN)
c.ready()

## Import immobile addictional object in ambient if models file exists
exists_work_ambient = False
work_ambient = list()

def loadAmbient():

	import os
	import sys

	global work_ambient, exists_work_ambient
	
	if os.path.exists("models/ambient"):
		# Import ambient list file
		sys.path.append("models/ambient")

		def isSTL(m):
			if (".stl" in m) or (".STL" in m): return True
			else: return False
		def isOBJ(m):
			if (".obj" in m) or (".OBJ" in m): return True
			else: return False

		try: from ambient import ambient_models
		except: print("Ambient list file not found!")

		for m in ambient_models:			
			if "show" in m:
				current = None
				if m["show"]:
					try:
						if isSTL("models/ambient/"+m["filename"]):
							current = AsciiSTL("models/ambient/"+m["filename"])
						elif isOBJ("models/ambient/"+m["filename"]):
							current = AsciiOBJ("models/ambient/"+m["filename"])

						if "color" in m:
							ci=m["color"]
							color = [ci[0]/255.0,ci[1]/255.0,ci[2]/255.0,ci[3]/255.0]
							current = Color(color,[current])

						if "translate" in m:
							current = Translate([current],0,0,float(m["translate"][0]))
							current = Translate([current],0,float(m["translate"][1]),0)
							current = Translate([current],float(m["translate"][2]),0,0)

						if "rotate" in m:
							current = Rotate([current],float(m["rotate"][0]),1,0,0);
							current = Rotate([current],float(m["rotate"][1]),0,1,0);
							current = Rotate([current],float(m["rotate"][2]),0,0,1);
						
						work_ambient.append(current)
					except: pass
						
		print("Found "+ str(len(work_ambient)) + " addictional ambient models")
		if len(work_ambient) > 0:
			work_ambient = Collection(work_ambient)
			exists_work_ambient = True


loadAmbient()

## Create Floor
if debug_orig_axis:
	# end effector X-Y-Z cross reference for debug
	floor = Collection([
        	Box(-200,-200,-3,120,120,0),
       		Color(refx_color,[CylinderX(0,5,200,2)]),
		Color(refy_color,[CylinderY(0,5,200,2)]),
       		Color(refz_color,[CylinderZ(0,5,200,2)])
        ])
else:
	floor = Collection([Box(-120,-120,-3,120,120,0)])

## Create Work
work = Capture()

## Create Tool
tool = Capture()

### Create Tooltip, tool with tip is attached to link7
tooltip = Capture()
# Create tip, show simple cone to indicate the position
# add 10mm for visualization only, tip start on internal link7
tip = Color(tip_color,[CylinderZ(0,3,toolZ_offset+49,0.4)])
# Translate it, return to tool origin
tip = Translate([tip],0,0,-(toolZ_offset+49))

if debug_orig_effector:
	effxaxis = Color(refx_color,[CylinderX(0,0.5,50,0.5)])
	effyaxis = Color(refy_color,[CylinderY(0,0.5,50,0.5)])
	effzaxis = Color(refz_color,[CylinderZ(0,0.5,50,0.5)])
	# Attach tooltip to tool and debug: final effector reference axis
	tool = Collection([tooltip, tool, tip ,effxaxis,effyaxis,effzaxis])
else:
	# Attach tooltip to tool
	tool = Collection([tooltip, tool , tip])

### Create link7 , this is a dummy Link, IMAGObot has 5DOF
link7 = AsciiSTL(filename="models/robot/link7.stl")
link7 = Color(tooltip_color,[link7])
# Translate it, note 49mm is the distance from tooltip to joint6
link7 = Translate([link7],0,0,-(49+toolZ_offset))
link7 = Rotate([link7],-180,0,0,1);
# Join to tool
link7 = Collection([link7, tool])
# Move back, joint6 rotate in origin
link7 = Translate([link7],0,0,49+toolZ_offset)
# Apply a dummy HAL DOF to join6
link7 = HalRotate([link7],c,"joint6",0,0,0,0)

### Create link6
link6 = AsciiSTL(filename="models/robot/link6.stl")
link6 = Color(default_color,[link6])
# Rotate and traslate it, note 41mm is the distance from join5 to join6
# 41 + 49 = 90mm is the L7+L6 distance (from tooltip to joint5)
link6 = Rotate([link6],-90,0,1,0)
link6 = Translate([link6],0,0,-41) 
# Join link7 to link6
link6 = Collection([link7, link6])
# Move back, joint5 rotate in origin
link6 = Translate([link6],0,0,41)
# Apply HAL DOF to joint5
link6 = HalRotate([link6],c,"joint5",1,1,0,0)

### Create link5
link5 = AsciiSTL(filename="models/robot/link5.stl")
link5 = Color(default_color,[link5])
# Rotate and traslate it
link5 = Translate([link5],0,0,-95)
# Join link6 to link 5
link5 = Collection([link6, link5])
# Move back, joint4 rotate in origin
link5 = Translate([link5],0,0,95)
# Apply HAL DOF to joint4
link5 = HalRotate([link5],c,"joint4",1,0,0,1)

### Create link4
link4 = AsciiSTL(filename="models/robot/link4.stl")
link4 = Color(default_color,[link4])
# Rotate and Traslate it, note 127.5 is L4 from joint4 and joint5
link4 = Rotate([link4],90,1,0,0)
link4 = Rotate([link4],-90,0,1,0)
link4 = Rotate([link4],90,0,0,1)
link4 = Translate([link4],0,0,-127.5)
# Join link5 to link4
link4 = Collection([link5, link4])
# Move back, joint3 rotate in origin
link4 = Translate([link4],1.85,0,127.5)
# Rotate it , load model with elbow to negative Z position
link4 = Rotate([link4],-90,1,0,0)
# Apply HAL DOF to joint3
link4 = HalRotate([link4],c,"joint3",1,1,0,0)

### Create link3
link3 = AsciiSTL(filename="models/robot/link3.stl")
link3 = Color(default_color,[link3])
# Rotate and Traslate it, note 221.12 is L2 from joint2 and joint3
link3 = Rotate([link3],  90,0,1,0)
link3 = Rotate([link3], 180,0,0,1)
link3 = Rotate([link3], 180,1,0,0)
link3 = Translate([link3],0,0,-221.12)
# Join link4 to link3  
link3 = Collection([link4, link3])
# Move back, joint3 rotate in origin
link3 = Translate([link3],0,0,221.12)
# Apply HAL DOF to joint2
link3 = Rotate([link3],-90,1,0,0)
# Rotate it , load model with "" to negative Z position
link3 = HalRotate([link3],c,"joint2",1,1,0,0)

### Create link3
link2 = AsciiSTL(filename="models/robot/link2.stl")
link2 = Color(default_color,[link2])
# Rotate and Traslate it, note 231.5 is L1 from joint1 and joint2
link2 = Rotate([link2], -90,0,0,1)
link2 = Rotate([link2], -90,0,1,0)
# Join link3 to link2
link2 = Collection([link3, link2]) 
# Set X in true X direction
link2 = Rotate([link2], -90,0,0,1)
# Apply HAL DOF to joint1
link2 = HalRotate([link2],c,"joint1",1,0,0,1)
# Traslate it, return to origin, link2 rotate around origin
link2 = Translate([link2],0,0,231.5)

### Create link1, stationary base
link1 = AsciiSTL(filename="models/robot/link1.stl");
link1 = Color(base_color,[link1])
link1 = Rotate([link1], 180,0,0,1)

### IMAGObot object, assembly link1 to link2
IMAGObot = Collection([link2, link1])
if exists_work_ambient:
	model = Collection([tooltip, IMAGObot, floor, work, work_ambient])
else:
	model = Collection([tooltip, IMAGObot, floor, work])

### Main Scene
main(model, tooltip, work,1270,1270,None,-75,600)

