# Preparation
In order to allow the bluetooth acting as a serial reader you need to edit

    sudo vi /etc/systemd/system/dbus-org.bluez.service

Find the following line and add a compatibility flag '-C' to the end:

    ExecStart=/usr/lib/bluetooth/bluetoothd -C

Additionally, add the following line after the above:

    ExecStartPost=/usr/bin/sdptool add SP

Save and reboot. Then connect to the device with terminal via:

    sudo rfcomm watch hci0

Check this: https://raspberrypi.stackexchange.com/questions/51548/raspberry-pi-3-bluetooth-pairing-issue-with-tablet

Use the Android app: "BlueTooth Serial Controler"
For the GPS sharing, use the Android app: "Share GPS"

# AutoAstroGuia
Software for the auto-astroguide project.

You need a raspberry pi with bluetooth. A green (astronomical) laser, a led, a relee, two servos (ALT/AZM).

The *run.py* script executes everything. The device connects to the mobile phone and gets the GPS coordinates.

The device recieves commands from the mobile phone through bluetooth and points the laser towards the desired astronomical object.

The catalog contains more than 4000 deep-sky objects and more than 200000 stars.
