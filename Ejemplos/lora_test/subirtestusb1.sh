#!/bin/bash
echo 'ingrese modo emisor o receptor'
read var1
echo "ingreso modo {$var1}"

#cd mainclient | sudo ampy -p /dev/ttyUSB0 put main.py

case $var1 in
	emisor)
		cd mainclient
		sudo ampy -p /dev/ttyUSB1 put main.py
		echo 'client subido ...'
		cd ..
		sudo ampy -p /dev/ttyUSB1 put all/LoRaSender.py
		echo 'LoRaSender subido ...'
		;;
	receptor)
		cd mainserver
		sudo ampy -p /dev/ttyUSB1 put main.py
		echo 'server subido ...'
		cd ..
		sudo ampy -p /dev/ttyUSB1 put all/LoRaReceiver.py
		echo 'LoRaReciver subido ...'
		;;
	*)
		echo "ingrese correctamente"
		;;
esac

sudo ampy -p /dev/ttyUSB1 put all/config_lora.py
echo 'config_lora subido ...'
sudo ampy -p /dev/ttyUSB1 put all/controller.py
echo 'controller subido ...'
sudo ampy -p /dev/ttyUSB1 put all/controller_esp32.py
echo 'controller_esp32 subido ...'
sudo ampy -p /dev/ttyUSB1 put all/sx127x.py
echo 'sx127x subido ...'
sudo ampy -p /dev/ttyUSB1 put all/ssd1306.py
echo 'Pantalla_i2c subido ...'

