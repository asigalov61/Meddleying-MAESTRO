### Basic instructions:

Install all requirements from requirements

Use MM_RaspiAudio_MIC+.sh to run on startup to control the generation and the playback with the RaspiAudio button.
Simply add MM_RaspiAudio_MIC+ to chron (sudo crontab -e) or /etc/rc.local
***
I.e. for chron:

@reboot /home/pi/MM_RaspiAudio_MIC+.sh
***
or for rc.local

sudo bash /home/pi/MM_RaspiAudio_MIC+.sh
***
And if you want to replace default Timidity SF2, simply copy yours to /usr/share/sounds/sf/FluidR3_GM.sf2
i.e.

cp font.sf2 /usr/share/sounds/sf/FluidR3_GM.sf2
***
### Hardware

1) ONE Raspberry Pi 4 Model B 2019 Quad Core 64 Bit WiFi Bluetooth (4GB)
2) ONE Audio DAC HAT Sound Card (Audio+Speaker+MIC) for Raspberry Pi4 /Pi Zero / Pi3 / Pi3B / Pi3B+ / Pi2 / Better Quality Than USB
3) ONE 3.5A Raspberry Pi 4 Power Supply with Switch (USB-C)
4) ONE USB 2.0 Mini Microphone for Raspberry Pi 4 Model B
5) TWO 2.4G Mini Wireless Keyboard with Touchpad Mouse,Lightweight Portable Wireless Keyboard Controller with USB Receiver Remote Control
6) Whatever else is compatible with everything above that you want to add/try
7) Do not forget to buy a suitable micro-SD card for Raspberry

