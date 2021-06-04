# Speranza-Cieca
![banner](https://github.com/PracticalHarware/Website/blob/main/Moody%20Mountains%20-%20Canva%20Banner.gif)
# Languages:
<p align="center">
    <img alt="python" src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white">
    <img alt="C++" src="https://img.shields.io/badge/C%2B%2B-00599C?style=for-the-badge&logo=c%2B%2B&logoColor=white">
    <img alt="Shell Script" src="https://img.shields.io/badge/Shell_Script-121011?style=for-the-badge&logo=gnu-bash&logoColor=white">
    
</p>

# Frameworks
<p align="center">
    <img alt="OpenCv" src="https://img.shields.io/badge/OpenCV-27338e?style=for-the-badge&logo=OpenCV&logoColor=white">
</p>

# Operating System
<p align="center">
    <img alt="Debian" src="https://img.shields.io/badge/Debian-A81D33?style=for-the-badge&logo=debian&logoColor=white">
</p>

# Hardware Used
<p align="center">
 <img alt="Raspberry Pi" src="https://img.shields.io/badge/RASPBERRY%20PI-C51A4A.svg?&style=for-the-badge&logo=raspberry%20pi&logoColor=white">
 <img alt="Arduino" src="https://img.shields.io/badge/Arduino_IDE-00979D?style=for-the-badge&logo=arduino&logoColor=white">
</p>
    
# Setup On Raspberry Pi (You can use the Batch files given too)

## STEP 1:-


    1.	Log into raspberry pi command prompt. 
    2.	At the Home directory get into configuration mode to expand directory 
        $ sudo raspi-config 
    3. Select the ‘advance Option’ 
    4. Choose ‘ Expand Filesystem’ and hit ‘Enter’ 
    5. Arrow down to finish. 
    6. You need reboot for change to take place, you would be prompted if not execute command 
        $ sudo reboot. 

    7. The first step is to update and upgrade any existing packages: 
        $ sudo apt-get update && sudo apt-get upgrade 

    Would be required, if you are using an existing raspberry pi stretch install to ensure, that you are updating all packages 
 
## STEP 2:-

    1. Install some developer tools, including CMake, which helps us configure the OpenCV build process: 
        $  sudo apt-get install build-essential cmake pkg-config 

    2.	Next, install some image I/O packages that allow us to load various image file formats from disk. Examples of such file formats include JPEG, PNG, TIFF, etc.: 
        $ sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev 

    3.	We also need video I/O packages. These libraries allow us to read various video file formats from disk as well as work directly with video streams: 
        $ sudo apt-get install libavcodec-dev libavformat-dev libswscaledev libv4l-dev 

        $ sudo apt-get install libxvidcore-dev libx264-dev 

    4.	Open library has high GUI module and important as well, to display images to screen. Towards this GTK library. 
        $ sudo apt-get install libgtk2.0-dev libgtk-3-dev 

    5.	Towards matrix operation and optimization of various packages  
        $ sudo apt-get install libatlas-base-dev gfortran 

    6.	Finally, let’s install both the Python 2.7 and Python 3 header files so we can compile OpenCV with Python bindings:           
        $ sudo apt-get install python2.7-dev python3-dev 
 
## STEP 3:- Download OpenCV (version 3.3) 
 
    1.	Download opencv  
    $ cd ~ 
    $ wget -O opencv.zip https://github.com/Itseez/opencv/archive/3.3.0.zip 
    $ unzip opencv.zip 

    2.	Download associated libraries  for additional features. 
    $ wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/3.3.0. zip 
    $ unzip opencv_contrib.zip 

## Step 4: Python 2.7 / Python 3 & dependencies 
 
    1.	User of pip tools get/ update: 
    $ wget https://bootstrap.pypa.io/get-pip.py 
    $ sudo python get-pip.py 
    $ sudo python3 get-pip.py 

    2.	Python dependency is NumPy 
    Note : This may take about 10~20 minutes: 
    $ pip install numpy 

    Step 5: Compile and install Open CV 
 
    1.	Set up and configure build  
    $ cd ~/opencv-3.3.0/ 
    $ mkdir build 
    $ cd build 
    $ "cmake -D CMAKE_BUILD_TYPE=RELEASE \ 
        -D CMAKE_INSTALL_PREFIX=/usr/local \ 
        -D INSTALL_PYTHON_EXAMPLES=ON \ 
        -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-
    3.3.0/modules \ 
        -D BUILD_EXAMPLES=ON .. 

    2.	Increase your swap space size. This enables OpenCV to compile with all four cores of the Raspberry PI without the compile hanging due to memory problems. 
        a.	Open your /etc/dphys-swapfile  and then edit the CONF_SWAPSIZE  variable: 
        b.	Once file is open. 
        c.	# CONF_SWAPSIZE=100 
        d.	CONF_SWAPSIZE=1024 
        e.	Save file 

    3.	Activate the new swap space, restart the swap service 
        $ sudo /etc/init.d/dphys-swapfile stop 
        $ sudo /etc/init.d/dphys-swapfile start 

    Note:  It is highly recommended that you change this setting back to the default when you are done compiling 

    4.	Compile OpenCV 
        a. $ make 
              OR 
        a. $ make -j4 

    Note:  
        1.	Either one of the above to be executed. The make -j4 would be using 4 cores, but prone to race condition / hang. The advantage could be faster completion. 
        2.	Just make alone, may take about 4~5 hours to complete 

    5.	Install / copy OpenCV 3 on your Raspberry Pi 3 location: 
        $ sudo make install 
        $ sudo ldconfig 


    6.	Find out site package file by listing. 
        $ ls -l /usr/local/lib/python3.5/site-packages/ 

    You would find file named: 
    cv2.cpython-35m-arm-linux-gnueabihf.so 

    7.	This file need to be renamed 
        $ cd /usr/local/lib/python3.5/site-packages/ 
        $ sudo mv cv2.cpython-35m-arm-linux-gnueabihf.so cv2.so 
 
Note: In some installation it would be as dist-packages. If its distpackages, replace site-packages to dist-packages 

### Testing: 

      $ python3       
        >>> import cv2 
        >>> cv2.__version__ 
             '3.3.0' 
          >>> 

### Caution note :  
    Don’t forget to change your swap size back! 

    Open your  /etc/dphys-swapfile  and then edit the  CONF_SWAPSIZE  variable:          CONF_SWAPSIZE=100 
