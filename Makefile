export AMPY_PORT=/dev/ttyUSB0
all:
	@echo "Usa make deploy para subir todos los archivos"
	@echo "Para borrar los archivos de la placa, usa make erase"
	@echo "Por defecto, el puerto asociado es /dev/ttyUSBO"
deploy:
	@-ampy mkdir drivers > /dev/null  #de esta forma el warning generado cuando la carpeta ya existe se descarta
	@echo 'Ingrese Numero ID collar'
	@read var_id
	@echo 'dirCollar = ' ${var_id} > direccionCollar.py

	#-----DRIVERS-----#

	##DRIVERS IMU
	ampy put imu/mpu6050.py drivers/mpu6050.py
	ampy put imu/constants.py drivers/constants.py
	ampy put imu/cfilter.py drivers/cfilter.py

	##DRIVERS SD
	ampy put sd/sdcard.py drivers/sdcard.py

	##DRIVERS PANTALLA
	ampy put pantalla_oled/ssd1306.py drivers/ssd1306.py

	##DRIVERS LORA
	ampy put nodo_collar/all/config_lora.py drivers/config_lora.py
	ampy put nodo_collar/all/controller.py drivers/controller.py
	ampy put nodo_collar/all/controller_esp32.py drivers/controller_esp32.py
	ampy put nodo_collar/all/sx127x.py drivers/sx127x.py

	ampy put nodo_collar/all/direccionCollar.py drivers/direccionCollar.py
	ampy put nodo_collar/all/data_frame.py drivers/data_frame.py
	ampy put nodo_collar/all/cola.py drivers/cola.py



	#-----MAIN y BOOT-----#
	ampy put boot.py
	ampy put main.py
	#-----CLASES-----#
	ampy put clases/sd.py
	ampy put clases/mic.py
	ampy put clases/imu.py
	ampy put clases/menu.py
	ampy put clases/gps.py
	ampy put clases/lora.py

erase:
	-ampy rmdir drivers
	-ampy rm main.py
	-ampy rm boot.py
	-ampy rm sd.py
	-ampy rm mic.py
	-ampy rm imu.py
	-ampy rm menu.py
	-ampy rm gps.py
	-ampy rm lora.py
