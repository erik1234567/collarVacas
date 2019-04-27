from gps_upy import Gps_upy
import _thread
from sd import *
from imu import *
from time import sleep
from machine import Timer, deepsleep, Pin

# led
#pinled = Pin(25, Pin.OUT)
#pinvext = Pin(21, Pin.OUT)

pinled.value(1)

# Modulo SD
sd = initSD()

# Modulo GPS
gps = Gps_upy()
gps.attachSD(sd)
gps.req_pos()

# Modulo IMU
imu = IMU()
imu.attachSD(sd)
imu.writesamples()

# se va a dormir 20 min
deepsleep(1.2E6)

#deepsleep(10*1000)