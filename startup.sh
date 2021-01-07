#!/bin/bash 

pactl set-default-sink 'alsa_output.usb-C-Media_Electronics_Inc._USB_Audio_Device-00.analog-stereo'
pactl -- set-sink-volume 0 90%
python3 ~/seeing_eye/main.py