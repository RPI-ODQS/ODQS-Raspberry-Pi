#!/usr/bin/python
#--------------------------------------   
# This script reads data from a 
# MCP3008 ADC device using the SPI bus.
#
##--------------------------------------

import pigpio
from math import sqrt


class PressureAndCurent:
	
	# static data
	_started = False
	_closed = True
	_refcount = 0
	_ADC2 = None
	
	def __init__(self, pi):
		#_refcount = 0
		#raise RuntimeError('!!!!!Close not called in Pio object')
		
		if (PressureAndCurent._refcount == 0):
			self.pi = pi
			PressureAndCurent.ADC2 = self.pi.spi_open(1, 75000, 0) # CE0, main SPI
			
		PressureAndCurent._refcount += 1
		self._closed = False
		PressureAndCurent._started = True
		
		
	def close(self):
		PressureAndCurent._refcount -= 1
		self._closed = True

		if PressureAndCurent._refcount == 0:
			self.pi.spi_close(PressureAndCurent.ADC2)
			PressureAndCurent._started = False
         
	def __del__(self):
		if not self._closed:
			self.pi.spi_close(PressureAndCurent.ADC2)
			PressureAndCurent._refcount = 0
			raise RuntimeError('!!!!!Close not called in Pio object')
		
	# Function to read SPI data from MCP3008 chip
	# Channel must be an integer 0-7
	# 0-1 for pressure
	def ReadChannel(self, channel):
	  
		(count, adc) = self.pi.spi_xfer(PressureAndCurent.ADC2, [1,(8+channel)<<4,0])
		if count == 3:	
			data = ((adc[1]&3) << 8) | adc[2]
		else:
			#print("bad reading {:b}".format(adc))
			print("Bad readings")
			data = 0
		return data
	  
	  
class Pressure(PressureAndCurent):
	
	def __init__(self, pi,bias_low_pressure = 0, bias_high_pressure = 0):
		PressureAndCurent.__init__(self, pi)
		self.pi = pi
		if not self.pi.connected:
			print("Pigpio error")
			exit(0)

		
		self.maxPressure = 1.2 # 1.2 MPa
		self.bias_low_pressure = bias_low_pressure
		self.bias_high_pressure = bias_high_pressure
		
	# the MCP3008 is 10 bit
	# 10bit means 1023 max analog reading
	# pressure sensor reading are from 0.5V to 4.5V.
	# This means 0.5V is 0(zero) MPa, 4.5V is 1.2MPa
	# 0.5V - 1023/10 = 102
	# 4.5V-0.5V = 4V - 1023/5 = 204
	# 4.5V-0.5V = 4V - means that 4V deiifrence corresponds to 1.2MPa difference
	# PRI3 max voltage is 3.3 but calculations are valid
	def ConvertPressure(self, sensorLevel, places):
		prs = (1.0*(sensorLevel-(102 + self.bias_low_pressure))/(204 + self.bias_high_pressure)) * self.maxPressure
		prs = round(prs,places)
		return prs
		
		
	# pres_chanel = 0 or 1
	def getPressure(self, pres_chanel):

		t=[]
		for readings in range(20):
			t.append(PressureAndCurent.ReadChannel(self, pres_chanel))
		t.sort()
		pres_level = sum(t[3:16])/float(14) # 14 elements are left when You remove 3 elemens from the begin and 3 elements from the tail of sorted array
		pressure = self.ConvertPressure(pres_level, 2)
		return pressure

  
	def delete(self):
		PressureAndCurent.close(self)
		#self.pi.spi_close(self.ADC2)

class Current(PressureAndCurent):
	
	def __init__(self, pi):
		PressureAndCurent.__init__(self, pi)
		self.pi = pi
		if not self.pi.connected:
			print("Pigpio error")
			exit(0)
			
		self.SupplyVoltage=3.3
		self.offsetI = 512
		self.ICAL = 0.5*17 # CT Ratio / Burden resistance = 800 / 47 Ohm
		



#-----------------------------------------------

	def calcIrms(self, currentChanel, Number_of_Samples):
		currentChanel += 4
		sumI = 0
		self.offsetI = 512
		for  n in range(Number_of_Samples):
			sampleI = PressureAndCurent.ReadChannel(self, currentChanel)
		
			# Digital low pass filter extracts the 2.5 V or 1.65 V dc offset,
			#  then subtract this - signal is now centered on 0 counts.
			self.offsetI = (self.offsetI + (sampleI-self.offsetI)/1024)
			filteredI = sampleI - self.offsetI

			# Root-mean-square method current
			# 1) square current values
			sqI = filteredI * filteredI
			# 2) sum
			sumI += sqI
			
		I_RATIO = self.ICAL *(self.SupplyVoltage / float(1024))
		Irms = I_RATIO * sqrt(sumI / Number_of_Samples)
		return Irms

	def delete(self):
		PressureAndCurent.close(self)
		#self.pi.spi_close(self.ADC2)
