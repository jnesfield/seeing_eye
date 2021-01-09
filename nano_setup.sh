#!/bin/bash
#initial setup - choose autologin otherwise it will cause problems later with lxdm:

apt-get purge -y libreoffice* 

apt-get clean 

apt-get install -y python3-pip 

apt-get install -y tesseract-ocr 

apt-get install -y libhdf5-serial-dev hdf5-tools libhdf5-dev zlib1g-dev zip libjpeg8-dev liblapack-dev libblas-dev gfortran 

yes | pip3 install  --upgrade pip 

yes | pip3 install  --upgrade Pillow 

yes | pip3 install pytesseract  

yes | pip3 install pyttsx3 

apt-get install -y espeak

#create startup script
#write out current crontab
crontab -l > mycron
#echo new cron into cron file
echo @reboot ~/seeing_eye/startup.sh >> mycron
#install new cron file
crontab mycron
rm mycron

chmod 777 ~/seeing_eye/startup.sh

apt-get install xserver-xorg-video-dummy

cp /etc/X11/xorg.conf /etc/X11/xorg.conf.old

rm /etc/X11/xorg.conf

cp ~/seeing_eye/xorg.conf /etc/X11/xorg.conf

