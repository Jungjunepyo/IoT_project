# IoT_project

## This is IoT project from Team 9, "Design of IoT systems" course in Ajou University, 2019 2nd semester.
This project is for collecting fine dust density in roadside atmosphere by Raspberry pi by attaching it to city bus and sends collected data to those who need it.

* This project requires at least two Raspberry pi devices.

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


__testbleemit.py__ should run in RPi which is used for bus station (beaconing) puropse, and __scanAndSend2.py__ should run in RPi which is used for bus purpose.

__dustServer.py__ and __mqtt_shadow.py__ should run in device(PC is recommended) which is used for CoAP server purpose.
