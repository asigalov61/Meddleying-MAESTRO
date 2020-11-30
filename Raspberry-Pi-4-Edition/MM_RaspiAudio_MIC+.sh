#!/bin/bash
#init led & button
echo 25 >/sys/class/gpio/unexport
echo 25 >/sys/class/gpio/export
echo out >/sys/class/gpio/gpio25/direction
echo 23 >/sys/class/gpio/export
echo in >/sys/class/gpio/gpio23/direction
#infinite loops
while [ 1 ]
do
while [ 1 ]
do
#led ON
cd ./Meddleying-MAESTRO/

python3 /home/pi/Meddleying-MAESTRO/MM_Generator.py
sleep 10
echo 1 >/sys/class/gpio/gpio25/value

echo  "------Please press the on Yellow button to listen to your composition"

amixer set Micro 50%
amixer set Master 99%
sudo alsactl store

#waiting button pressed
while [ `cat /sys/class/gpio/gpio23/value` = 1 ]; do
set i = 1
done
#led OFF
echo 0 >/sys/class/gpio/gpio25/value

#led BLINK
echo 1 >/sys/class/gpio/gpio25/value
sleep 1
echo 0 >/sys/class/gpio/gpio25/value
sleep 1
echo 1 >/sys/class/gpio/gpio25/value
sleep 1
echo 0 >/sys/class/gpio/gpio25/value
sleep 1
echo 1 >/sys/class/gpio/gpio25/value
sleep 1
echo 0 >/sys/class/gpio/gpio25/value


echo "Playing the output MIDI file..."
#play record
timidity /home/pi/Meddleying-MAESTRO/output.mid
done
echo "------------------------------------------------------------------------"
done
exit

done
echo 25 >/sys/class/gpio/unexport


