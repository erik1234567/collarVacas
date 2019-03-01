"""
    Proceso automatico para guardar informacion del modulo GPS y acelerometro en la tarjeta SD
"""
from machine import I2C, Pin, SPI, UART
"""import os
import time
import mpu6050	
import micropython
import sdcard
import ssd1306

micropython.alloc_emergency_exception_buf(100)
"""
#####################################Inicializacion de modulos######################################
#objeto MPU
#mpu = mpu6050.MPU()
#objeto UART/GPS
#gps = UART(2, 115200)
gps = UART(2, 9600)
#gps.init(9600,bits=8,parity=None,stop=1,tx=17,rx=5)
gps.init(9600,bits=8,parity=None,stop=1,tx=5,rx=18)
# configuracion de modo de poder GPS
print(str(gps.readline()))
gps.write(b'$PMTK001,101,0*33<CR><LF>')
print(str(gps.readline()))
gps.write(b'$PMTK225, 0*0B<CR><LF>')
print(str(gps.readline()))
gps.write(b'$PMTK223,1,25,180000,60000*38<CR><LF>')
print(str(gps.readline()))
gps.write(b'$PMTK225,1,3000,12000,18000,72000*16<CR><LF>')
print(str(gps.readline()))

"""
#objeto SPI
Pin(18,Pin.OUT,value=1) #para desactivar LoRa
spi = SPI(sck=Pin(23),miso=Pin(14),mosi=Pin(13))
#objeto SD
sd = sdcard.SDCard(spi, Pin(2,Pin.OUT))
oled.text('SD...OK', 0, 20)
oled.show()

# contador auxiliar para controlar numero de ciclos
cont = 1

################################################loop################################################
while 0:
    #se monta el sistema de archivos en la sd
    os.mount(sd, '/fc')
    print('Filesystem check')
    print(os.listdir('/fc'))
    # INFORMACION MODULO GPS
    aux = gps.readline()
    gps_data = str(aux)
    oled.text('Escribiendo SD', 0, 30)
    oled.show()
    filename = '/fc/gps_data.txt'
    with open(filename,'a') as f:
        n = f.write('{}\n'.format(gps_data))
        print(n, 'bytes written')
    # INFORMACION MODULO ACELEROMETRO
    aux = mpu.read_sensors_scaled()
    aux = aux[0] + aux[1] + aux[2]
    accelerometer_data = str(aux)
    filename = '/fc/accelerometer_data.txt'
    # el parametro 'a' deriva de 'append' (adjuntar)
    with open(filename,'a') as f:
        n = f.write('{},'.format(accelerometer_data))
        print(n, 'bytes written')
    
    os.umount('/fc')
    time.sleep(0.8)
    Pin(25, Pin.OUT, value=0)
    time.sleep(0.8)
    Pin(25,Pin.OUT, value=1)
    #reseteo pantalla
    oled.fill(0)
    #contador (solo para debug)
    cont = cont + 1
    #if cont > 20:
    #    oled.text('Escribiendo SD', 0, 30)
    #    oled.show()
    #    break

# Proceso terminado
oled.fill(0)
oled.text('Fin, Todo OK', 5, 45)
oled.show()

"""