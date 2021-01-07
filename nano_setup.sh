#!/bin/bash
#initial setup - choose autologin otherwise it will cause problems later with lxdm:

apt-get purge -y libreoffice* 

apt-get clean 

apt-get install -y python3-pip 

apt-get install -y tesseract-ocr 

yes | pip3 install  flask 

yes | pip3 install  --upgrade pip 

yes | pip3 install  --upgrade Pillow 

yes | pip3 install pytesseract  

yes | pip3 install pyttsx3 

apt-get install -y libhdf5-serial-dev hdf5-tools libhdf5-dev zlib1g-dev zip libjpeg8-dev liblapack-dev libblas-dev gfortran 

yes | pip3 install -U pip testresources setuptools==49.6.0 

yes | pip3 install -U numpy==1.16.1 future==0.18.2 mock==3.0.5 h5py==2.10.0 keras_preprocessing==1.1.1 keras_applications==1.0.8 gast==0.2.2 futures protobuf pybind11 

apt-get install -y espeak

git lfs pull 

#create startup script
#write out current crontab
crontab -l > mycron
#echo new cron into cron file
echo @reboot ~/seeing_eye/startup.sh >> mycron
#install new cron file
crontab mycron
rm mycron

chmod 777 ~/seeing_eye/startup.sh

