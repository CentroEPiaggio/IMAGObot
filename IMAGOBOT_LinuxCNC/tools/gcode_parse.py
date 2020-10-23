#!/usr/bin/python
#
# Clear extruder line from an 3D printer gcode file
#
#
#
import sys
import re

f=open(sys.argv[1],"r")
out=open(sys.argv[1].replace(".gcode","") + "_mod.gcode","w")

for line in f:
	if line[0] == ';': pass
	if "M82" in line: pass
	if "G28" in line: pass
	if "M104" in line: pass
	if "M140" in line: pass
	if "M106" in line: pass
	if "M107" in line: pass
	else:
		if "E" in line:
			newline = re.sub(r'E.* ',"",line)
			newline = re.sub(r'E.*',"",newline)
			out.write(newline)
		else:
			out.write(line)


