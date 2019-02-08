import ssd1306
from machine import Pin, I2C
from direccionCollar import *
from time import time

Pin(16,Pin.OUT,value=1)
#led = Pin(25,Pin.OUT,value=1)
scl = Pin(15,Pin.OUT,Pin.PULL_UP)
sda = Pin(4,Pin.OUT,Pin.PULL_UP)
i2c = I2C(sda=sda,scl=scl,freq=450000)
display = ssd1306.SSD1306_I2C(128, 64, i2c)

paqueteEnviar = bytes(0)
paqueteActual = bytes(0)
intentosACK = 2
intentos = 0
paqueteSync = False
SYMB_TIME_OUT = 200


def collar(lora):
    print("LoRa Collar")
    lora.onReceive(on_receive)#Asigna una función para la interrupcion del pin DIO0
    lora.onTimeout(on_timeout,SYMB_TIME_OUT)#Asigna una función para la interrupcion del pin DIO1 y asigna un Timeout
    global display
    global paqueteActual
    global led
    display.fill(0)
    display.text("LoRa Collar",0,0)
    display.show()
    lora.receive()
    while True:
        tiempo=int(time())
        paqueteActual = bytes([0,2]) +bytes([(tiempo>>24)&0xff,(tiempo >> 16) & 0xff,(tiempo>>8)&0xff,tiempo & 0xff])

        # led.value(1)
        # time.sleep(0.1)
        # led.value(0)
        # time.sleep(0.1)
        pass;

def on_receive(lora,paquete):
    global intentos
    global display
    global paqueteActual
    global paqueteSync
    global paqueteEnviar
    display.fill(0)
    if paquete:
        direccion = paquete[0]
        if direccion == dirCollar:
            comando = paquete[1]
            #mensaje = paquete[2:].decode()
            display.text("Recibi:",0,10)
            if comando == 0:
                paqueteSync = True#llego un paquete de sincronización
                lora.bytesprintln(paqueteActual)
                paqueteEnviar = paqueteActual
                display.text("Sync",0,20)
                lora.receiveSingle()
            elif paqueteSync and (comando == 1):
                paqueteSync = False
                display.text("ACK",0,20)
                intentos = 0
                lora.receive()
        else:
            display.text("Direccion Diferente",0,10)
    else :
        display.text("Paquete con Error",0,10)
        lora.receive()
    if paqueteSync:
        lora.receiveSingle()
    display.text("RSSI:{0}".format(lora.packetRssi()),0,30)
    display.show()



def on_timeout(lora):
    global intentosACK
    global paqueteEnviar
    global intentos
    intentos += 1
    if intentos <= intentosACK:
        if paqueteSync:
            lora.bytesprintln(paqueteEnviar)
            lora.receiveSingle()#se espera nuevamente un ACK
    else:
        lora.receive()#intentos no cumplidos