from gps import Gps_upy
import _thread
from sd import *
from imu import *
from time import sleep
from machine import Timer, deepsleep, Pin, ADC
import uos
#from Clientecollar import LoRa
LOW_BAT_LEVEL = 1600


pinvext = Pin(21, Pin.OUT)
pinvext.value(0)

adc = ADC(Pin(32))
adc.atten(adc.ATTN_11DB)
adc.read() # se consume la primera lectura, ya que da una medicion erronea 
# promedio de muestras de adc
promedio = 0
for i in range(100):
	promedio = promedio + adc.read()
promedio = promedio / 100
	
# respaldo promedio

if promedio < LOW_BAT_LEVEL:
	deepsleep()

v_s = 3.6/4096*promedio
v_bat = (v_s-0.7)*16/5+0.7

sd = initSD()
if sd is not None:
	mount(sd, "/")
	v = open('tension.csv', 'a')
	v.write("{},{},\n".format(promedio,v_bat))
	v.close()
	umount("/")
# Modulo GPS
gps = Gps_upy()
gps.attachSD(sd)
gps.write2sd(120000)

# Modulo IMU
imu = IMU()
imu.attachSD(sd)
imu.writesamples()


################### MODO SLEEP ##################
deepsleep(60000)