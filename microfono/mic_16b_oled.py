#
# This file is part of the MicroPython ESP32 project
# 
# The MIT License (MIT)
#
# Copyright (c) 2019 Mike Teachman
#
# https://opensource.org/licenses/MIT

# This example reads audio samples from an I2S microphone and writes 
# them to a WAV file stored on an external SDCard.
#
# Testing was done with an Adafruit I2S MEMS Microphone Breakout - SPH0645LM4H
#
# Recording duration is configured using RECORD_TIME_IN_SECONDS
#
# Audio samples from the SPH0645LM4H device have 18 bit precision.  The prune() function
# takes the most significant two bytes of each sample (2 least significant
# bits are discarded in this operation)
#
# The example imports MicroPython module sdcard.py.  This module is located in 
# folder micropython/drivers/sdcard.  If the module is not present in the build
# it needs to be copied to the filesystem using a tool such as rshell or ampy

import uos
from drivers import sdcard
from machine import I2S
from machine import I2C
from machine import Pin
from machine import SPI
from drivers import ssd1306

SDCARD_SECTOR_SIZE = 512                    # typical sector size for SDCards, in bytes
SAMPLE_BLOCK_SIZE = SDCARD_SECTOR_SIZE * 4  #  
BYTES_PER_SAMPLE = 2
BITS_PER_SAMPLE = 16
SAMPLES_PER_SECOND = 16000
RECORD_TIME_IN_SECONDS = 4


Pin(21, Pin.OUT, value = 0)
Pin(16, Pin.OUT, value = 1)
scl = Pin(15, Pin.OUT, Pin.PULL_UP)
sda = Pin(4, Pin.OUT, Pin.PULL_UP)
i2c = I2C(scl=scl, sda=sda, freq=450000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
oled.fill(0)
oled.text("iniciando",4,4)
oled.text("grabacion...",4,4+8)
oled.show()


def prune(samples_in, samples_out):
    for i in range(len(samples_in) // 8):
        samples_out[2*i] = samples_in[8*i + 2]
        samples_out[2*i + 1] = samples_in[8*i + 3]    

def gen_wav_header(sampleRate, bitsPerSample, num_channels, num_samples):
    datasize = num_samples * num_channels * bitsPerSample // 8
    o = bytes("RIFF",'ascii')                                                   # (4byte) Marks file as RIFF
    o += (datasize + 36).to_bytes(4,'little')                                   # (4byte) File size in bytes excluding this and RIFF marker
    o += bytes("WAVE",'ascii')                                                  # (4byte) File type
    o += bytes("fmt ",'ascii')                                                  # (4byte) Format Chunk Marker
    o += (16).to_bytes(4,'little')                                              # (4byte) Length of above format data
    o += (1).to_bytes(2,'little')                                               # (2byte) Format type (1 - PCM)
    o += (num_channels).to_bytes(2,'little')                                    # (2byte)
    o += (sampleRate).to_bytes(4,'little')                                      # (4byte)
    o += (sampleRate * num_channels * bitsPerSample // 8).to_bytes(4,'little')  # (4byte)
    o += (num_channels * bitsPerSample // 8).to_bytes(2,'little')               # (2byte)
    o += (bitsPerSample).to_bytes(2,'little')                                   # (2byte)
    o += bytes("data",'ascii')                                                  # (4byte) Data Chunk Marker
    o += (datasize).to_bytes(4,'little')                                        # (4byte) Data size in bytes
    return o


WAV_DATA_SIZE = RECORD_TIME_IN_SECONDS * SAMPLES_PER_SECOND * BYTES_PER_SAMPLE
wav_header = gen_wav_header(SAMPLES_PER_SECOND, BITS_PER_SAMPLE, 1, SAMPLES_PER_SECOND * RECORD_TIME_IN_SECONDS)

bck_pin = Pin(25)
ws_pin = Pin(27)
sdin_pin = Pin(35)

#bck_pin = Pin(25)
#ws_pin = Pin(27)
#sdin_pin = Pin(26)

audio_out = I2S(I2S.NUM0, bck=bck_pin, ws=ws_pin, sdin=sdin_pin, 
              standard=I2S.PHILIPS, mode=I2S.MASTER_RX,
              dataformat=I2S.B32, channelformat=I2S.ONLY_RIGHT,
              samplerate=SAMPLES_PER_SECOND*2,
              dmacount=8, dmalen=256)

Pin(18,Pin.OUT, value=1)
spi = SPI(sck=Pin(23), mosi=Pin(12), miso=Pin(14))
try:
    sd = sdcard.SDCard(spi, Pin(2,Pin.OUT))
    vfs =uos.VfsFat(sd)
    uos.mount(vfs, "/sd")    
except Exception as e:
    oled.fill(0)
    oled.text("error al montar sd",4,12)
    oled.show()
    audio_out.deinit()
    spi.deinit()
    raise e


s = open('/sd/mic_recording.wav','wb')
s.write(wav_header)

mic_samples = bytearray(SAMPLE_BLOCK_SIZE)
sd_samples = bytearray(SDCARD_SECTOR_SIZE)
numread = 0
numwrite = 0

for _ in range(WAV_DATA_SIZE // SDCARD_SECTOR_SIZE):
    try:
        numread = audio_out.readinto(mic_samples)    
        prune(mic_samples, sd_samples)
        numwrite = s.write(sd_samples)
    except KeyboardInterrupt:  
        break
s.close()
uos.umount("/sd")
spi.deinit()
audio_out.deinit()
oled.fill(0)
oled.text("Listo!", 64, 32)
oled.show()
print("listo: procesos terminados")
