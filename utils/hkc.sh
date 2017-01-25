#!/bin/bash

function usage() {
    cat <<-EOF
Usage: 
1. run xrandr to see which screen you want to adapter
"""
[geek@lwr utils]$ xrandr
Screen 0: minimum 8 x 8, current 1920 x 1968, maximum 32767 x 32767
eDP1 connected primary 1366x768+277+1200 (normal left inverted right x axis y axis) 310mm x 170mm
   1366x768      60.00*+  40.00  
   1280x720      60.00  
   1024x768      60.00  
   1024x576      60.00  
   960x540       60.00  
   800x600       60.32    56.25  
   864x486       60.00  
   640x480       59.94  
   720x405       60.00  
   680x384       60.00  
   640x360       60.00  
DP1 connected 1920x1200+0+0 (normal left inverted right x axis y axis) 600mm x 340mm
   1024x768      60.00 +
   1680x1050     59.95  
   1600x900      60.00  
   1280x1024     60.02  
   1440x900      59.89  
   1280x960      60.00  
   1366x768      59.79  
   1280x800      59.81  
   1152x864      59.97  
   1280x720      60.00  
   800x600       60.32  
   640x480       59.94  
   1920x1200_60.00  59.88*                                                                                                                        
HDMI1 disconnected (normal left inverted right x axis y axis)
HDMI2 disconnected (normal left inverted right x axis y axis)
VIRTUAL1 disconnected (normal left inverted right x axis y axis)
"""
2. choose the screen,(DP1)
3. adapt the screen DP1
"""
hkc.sh DP1
"""
EOF
}

function adapt() {
    if [ -z $1 ]; then
		usage
		exit
	fi
	vga=$1
	cvt 1920 1200
	xrandr --newmode "1920x1200_60.00"  193.25  1920 2056 2256 2592  1200 1203 1209 1245 -hsync +vsync
	xrandr --addmode $vga "1920x1200_60.00"
    #if [ -z $? ];then
	#	echo "set 1920 1200 success"
	#else
	#	usage
	#fi
}

function main() {
	adapt $1
}

main $1
