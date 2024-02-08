#!/bin/bash

cd /sys/kernel/config/usb_gadget/
mkdir -p isticktoit
cd isticktoit

echo 0x0100 > bcdDevice # v1.0.0
echo 0x0200 > bcdUSB # USB2
echo 0x2341 > idVendor # pretend leonardo
echo 0x8036 > idProduct # pretend leonardo

mkdir -p strings/0x409
echo "fedcba9876543210" > strings/0x409/serialnumber
echo "pi zero w HID" > strings/0x409/manufacturer
echo "iSticktoit.net USB Device" > strings/0x409/product

mkdir -p configs/c.1/strings/0x409
echo "Config 1: ECM network" > configs/c.1/strings/0x409/configuration
echo 250 > configs/c.1/MaxPower

# Add functions here
mkdir -p functions/hid.usb0
echo 1 > functions/hid.usb0/protocol
echo 1 > functions/hid.usb0/subclass
echo 8 > functions/hid.usb0/report_length

echo -ne \\x05\\x01\\x09\\x02\\xa1\\x01\\x09\\x01\\xa1\\x00\\x85\\x01\\x05\\x09\\x19\\x01\\x29\\x03\\x15\\x00\\x25\\x01\\x95\\x03\\x75\\x01\\x81\\x02\\x95\\x01\\x75\\x05\\x81\\x03\\x05\\x01\\x09\\x30\\x09\\x31\\x09\\x38\\x15\\x81\\x25\\x7f\\x75\\x08\\x95\\x03\\x81\\x06\\xc0\\xc0\\x05\\x01\\x09\\x06\\xa1\\x01\\x85\\x02\\x05\\x07\\x19\\xe0\\x29\\xe7\\x15\\x00\\x25\\x01\\x75\\x01\\x95\\x08\\x81\\x02\\x95\\x01\\x75\\x08\\x81\\x03\\x95\\x06\\x75\\x08\\x15\\x00\\x25\\x65\\x05\\x07\\x19\\x00\\x29\\x65\\x81\\x00\\xc0 > functions/hid.usb0/report_desc

ln -s functions/hid.usb0 configs/c.1/
# End functions

echo 0x80 > configs/c.1/bmAttributes
echo 200 > configs/c.1/MaxPower # 200 mA

sleep 2

ls /sys/class/udc > UDC

sleep 2

chmod 777 /dev/hidg0