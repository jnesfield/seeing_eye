# Seeing Eye #
## James L. Nesfield, MSBA ##
## 1/1/2021 ##

### INSPIRATION ###

**My mother is blind.** She has a degenerative condition called **Retinitis Pigmentosa**. There is no cure for this condition at this time. For as long as I can remeber she has had trouble seeing at night and difficulty with peripheral vision. In the last few years her sight has rapidly declined to the point where she can not read or do normal day to day activities. I wanted to develop a tool that would give her back some of her normality in life so she can at least identify some simple objects in her surroundings as well as read any labels or text on them. With that in mind and the Jetson Nano available i set to task to make this tool a reality.<br>

### SHOPPING LIST ###

The shopping list for this project is below with links to the actual items I purchased. The shopping list is broken down into two sections **CORE** and **OPTIONAL**. Most of the optional items are things I got that help the workflow but are not really necessary.<br>

#### CORE ####
**Jetson Nano 2GB Dev Kit:** https://www.amazon.com/NVIDIA-Jetson-Nano-Developer-945-13541-0000-000/dp/B08J157LHH/ref=sr_1_3?dchild=1&keywords=jetson+nano+2gb&qid=1609698418&sr=8-3<br>
**SD Card:** https://www.amazon.com/gp/product/B07G3H5RBT/ref=ppx_yo_dt_b_asin_title_o08_s00?ie=UTF8&psc=1<br>
**Electronic Parts Kit:** https://www.amazon.com/gp/product/B01IH4VJRI/ref=ppx_yo_dt_b_asin_image_o00_s00?ie=UTF8&psc=1<br>
**USB Audio Device:** https://www.amazon.com/gp/product/B00XM883BK/ref=ppx_yo_dt_b_asin_title_o01_s00?ie=UTF8&psc=1<br>
**Jumper Shunts:** https://www.amazon.com/gp/product/B077957RN7/ref=ppx_yo_dt_b_asin_title_o07_s00?ie=UTF8&psc=1<br>
**Atx Power Buttons:** https://www.amazon.com/gp/product/B07JYX97Y6/ref=ppx_yo_dt_b_asin_title_o07_s02?ie=UTF8&psc=1<br>
**USB C Power Supply:** https://www.amazon.com/gp/product/B07TYQRXTK/ref=ppx_yo_dt_b_asin_title_o09_s00?ie=UTF8&psc=1<br>
**1MP USb Camera:** https://www.amazon.com/gp/product/B00UMX3HEG/ref=ppx_yo_dt_b_asin_title_o07_s00?ie=UTF8&psc=1<br>

#### OPTIONAL ####
**Nano Case:** https://www.amazon.com/gp/product/B07TS83WGW/ref=ppx_yo_dt_b_asin_title_o08_s00?ie=UTF8&psc=1<br>
**Battery Pack:** https://www.amazon.com/gp/product/B07P5ZP943/ref=ppx_yo_dt_b_asin_title_o05_s00?ie=UTF8&psc=1<br>

Various other cabels and widgets are also involved. If I miss something big please comment so I can fix it!

### BASE SET UP ###
Follow the steps in the Nvidia documentation (https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit#write) to set up the Nano. On the build I am working on I used jetpack 4.4.1 found here: https://developer.nvidia.com/embedded/Jetpack. Please note during set up to select the option to auto login for the Nano as i have found it causes other issues down the road to not have such enabled!<br>
Once the Nano is set up follow the instructions in the file **nano_setup.txt** in this repository which lays out the commands to set up the software needed to run this project. There are some additional things in the set up like tensorflow, tensorflow hub, and juptyer which are not needed to run the application but are useful to build on top of this effort. The set up steps include removing the ubuntu desktop (memory hog) as well as installing *GIT LFS* to enable downloading the frozen models needed. It goes without saying if you are reading this that you should have some familarity with *GIT and GIT LFS*.<br>
After setting up the linux packages please follow the GPIO setup instructions at: https://github.com/NVIDIA/jetson-gpio. GPIO is needed later to enable a button to be used to tell the application when to capture an image to process.<br>
At this point you should be ready to go.

### GPIO SETUP ###
The GPIO set up follows the below schematic:

<img src="https://github.com/jnesfield/seeing_eye/blob/main/gpio%20pin%20schematic.PNG">

**In lay terms:** we are using pins 1, 9, and 15.<br> 
- Pin 1: 3.3 Volt
- Pin 9: Ground
- Pin 15: LCD_TE
<br>
By recreating this schematic with a bread board and some header wires we end up with the following:<br>

<img src="https://github.com/jnesfield/seeing_eye/blob/main/GPIO%20bread%20board.png">

Now we have a GPIO based button that will work with the application, provided the Jetson GPIO github instructions were followed correctly.

Next we set up a light that tells us when the application is ready folling this schematic:

<img src="https://github.com/jnesfield/seeing_eye/blob/main/light.png">

**In lay terms:** we are using pins 2, 9, and 23.<br> 
- Pin 2: 5 Volt
- Pin 9: Ground
- Pin 15: SPI_1_SCK
<br>

By recreating this schematic with a bread board and some header wires we end up with the following:<br>
*PLEASE NOTE: The button on the prior set up has been replaced by a atx case button with longer wires*

<img src="https://github.com/jnesfield/seeing_eye/blob/main/BUTTONnLIGHT.png">

**MORE TO COME**
