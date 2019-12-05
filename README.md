# IoT_project

### This is IoT project from Team 9

* This project require at least two Raspberry pi device.

To work with this project, you should install **blueZ** module in your RPi first.

    $ sudo apt-get -y install libusb-dev 
    $ sudo apt-get -y install libdbus-1-dev 
    $ sudo apt-get -y install libglib2.0-dev 
    $ sudo apt-get -y install libudev-dev 
    $ sudo apt-get -y install libical-dev 
    $ sudo apt-get -y install libreadline-dev 
    $ sudo apt-get -y install libdbus-glib-1-dev

    $ sudo mkdir bluez 
    $ cd bluez 
    $ sudo wget www.kernel.org/pub/linux/bluetooth/bluez-5.19.tar.gz 

    $ sudo gunzip bluez-5.19.tar.gz
    $ sudo tar xvf bluez-5.19.tar

    $ cd bluez-5.19
    $ ls

    $ sudo ./configure --disable-systemd
    $ sudo make 
    $ sudo make install 
    $ sudo apt-get install python-bluez 
    $ sudo shutdown -r now