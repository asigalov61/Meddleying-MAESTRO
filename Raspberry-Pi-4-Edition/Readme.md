
Install all requirements from requirements

Use MM_RaspiAudio_MIC+.sh to run on startup to control the generation and the playback with the RaspiAudio button.
Simply add MM_RaspiAudio_MIC+ to chron (sudo crontab -e) or /etc/rc.local

I.e. for chron:
@reboot /home/pi/MM_RaspiAudio_MIC+.sh

or for rc.local
sudo bash /home/pi/MM_RaspiAudio_MIC+.sh
