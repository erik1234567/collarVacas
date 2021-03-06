#!/usr/bin/env python
# objeto gps del cual se puede extraer info sobre la posicion
# ademas inicializa la comunicacion via UART con el gps

from machine import UART
from time import sleep
from uos import *

class Gps_upy(UART):
	def __init__(self):
		super(Gps_upy, self).__init__(2, 9600)
		super().init(9600, bits=8, parity=None, stop=2, tx=17, rx=33)
		# configurar gps a 9600 baud
		#super().write(b'$PMTK251,9600*27\r\n')

	def req_pos(self):
		super().write(b'$PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*29\r\n')
		sleep(1)

		while 1:
			self.frame = super().readline()
			self.pos = str(self.frame).split(',')
			try:
				if self.pos[2]=='A':
					break
			except IndexError:
				continue
			except:
				print('error desconocido')

		#self.pack = self.pos[3:7]
		self.pack = self.pos[3]+','+self.pos[4]+','+self.pos[5]+','+self.pos[6]
		print('data a escribir(GPS):')
		print(self.pack)
		# escritura en sd
		if self.sd is not None:
			mount(self.sd, "/")
			filename = '/gps_data.txt'
			with open(filename,'a') as f:
				n = f.write('{}\n'.format(self.pack))
			umount("/")
		else:
			print('sd no detectada')

	# Metodo para decodificar las sentencias GPRMC y GPGGA
	def decode(self, data):
		if(data[0]=='$GPRMC'):
			self.latitud = data[3]
			self.ref_latitud = data[4]
			self.longitud = data[5]
			self.ref_longitud = data[6]
		elif(data[0]=='$GPGGA'):
			# informacion sobre la posicion
			self.latitud = data[2]
			self.ref_latitud = data[3]
			self.longitud = data[4]
			self.ref_longitud = data[5]
		else:
			pass
	# modos de arranque (time to first fix)
	def cold_start(self):
		# modo por defecto del gps
		# busca almanaque
		super().write(b'$PMTK103*30\r\n')
	def full_cold_start(self):
		super().write(b'$PMTK104*37\r\n')
	def warm_start(self):
		# obtiene efemerides
		super().write(b'$PMTK102*31\r\n')
	def hot_start(self):
		# hot start
		super().write(b'$PMTK101*32\r\n')

	# Modos de energia
	def standby_mode(self):
		super().write(b'$PMTK161,0*28\r\n')
	def sleep_mode(self):
		super().write(b'$PMTK161,1*29\r\n')
	def periodic_mode(self):
		# ejemplo del data
		#super().write(b'$PMTK225,2,3000,12000,18000,72000*15\r\n')

		# my setup (7 segundos activo, 1 min dormido)
		#super().write(b'$PMTK225,2,7000,60000,0,0*18\r\n')

		# my setup 2.0 (7 seg on 14 seg off)
		#super().write(b'$PMTK225,8,7000,14000,0,0*11\r\n')

		# setup 3 (5 min on 15 min off)
		super().write(b'$PMTK225,2,180000,900000,0,0*29\r\n')


	def attachSD(self, sd):
		self.sd = sd
	def nmea_out(self):
		# solo GPRMC
		super().write(b'$PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*29\r\n')
		# resetear por defecto
		#super().write(b'$PMTK314,-1*04\r\n')

	# Modos sin testear
	def position_fix_interval(self):
		# este parametro controla la tasa de obtencion de posicion de gps (position fix freq)
		super().write(b'$PMTK500,1000,0,0,0,0*1A\r\n')

	def kill_data(self):
		super().write(b'$PMTK120*31\r\n')

	def request_efemerides(self):
		# busca en las efemerides 1800 seg atras
		super().write(b'$PMTK660,1800*17\r\n');
		#sleep()
		#return super().read()

#		super().write(b'')
