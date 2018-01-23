#!/usr/bin/python
#--------------------------------------   
# This script reads data from a 
# MCP3008 ADC device using the SPI bus.
#
##--------------------------------------

import pigpio
from math import log





class Temperature:
	
	def __init__(self, pi):
		self.pi = pi
		if not self.pi.connected:
			print("Pigpio error")
			exit(0)
		self.ADC1 = self.pi.spi_open(0, 75000, 0) # CE0, main SPI
		
	# Function to read SPI data from MCP3008 chip
	# Channel must be an integer 0-7
	def ReadChannel(self, channel):
	  
            (count, adc) = self.pi.spi_xfer(self.ADC1, [1,(8+channel)<<4,0])
	#adc = spi.xfer2([1,(8+channel)<<4,0])
            if count == 3:	
                data = ((adc[1]&3) << 8) | adc[2]
            else:
	    #print("bad reading {:b}".format(adc))
                print ("Bad readings")
                data = 0

            return data

	# Function to convert data to voltage level,
	# rounded to specified number of decimal places. 
	def ConvertVolts(self, data,places):
	  volts = (data * 3.3) / float(1023)
	  volts = round(volts,places)  
	  return volts
  
	# usefil links for this function
	def ConvertResistance(self, data,places):
	  Rseries = 10 #kOhms
	  Ohms = Rseries * (float(1023) / data - 1) #the case of pull down resistor
	  Ohms = round(Ohms,places)  
	  return Ohms
  
 
	# Function to calculate temperature from
	# NTC-MF52AT 10 K +/-1% 3950 (NTC-MF52-103 3950) data, rounded to specified
	# number of decimal places.
	def ConvertTemp(self, Resistance,places):
	  NOMINAL_RESISTANCE = 10 #kOhms
	  NOMINAL_TEMPERATURE = 25
	  BCOEFFICIENT = 3950
	  
	  #using a  B-parameter Equation which is a modification of the Steinhart-Hart equation
	  steinhart = Resistance / NOMINAL_RESISTANCE; # (R/Ro)
	  steinhart = log(steinhart); # ln(R/Ro)
	  steinhart /= BCOEFFICIENT; # 1/B * ln(R/Ro)
	  steinhart += 1.0 / (NOMINAL_TEMPERATURE + 273.15); # + (1/To)
	  steinhart = 1.0 / steinhart; # Invert
	  steinhart -= 273.15; # convert to C
	  
	  
	  
	  steinhart = round(steinhart,places)
	  return steinhart
  
	def delete(self):
		self.pi.spi_close(self.ADC1)


	def getTemp(self, temp_chanel):
		t=[]
		for readings in range(20):
			t.append(self.ReadChannel(temp_chanel))
		t.sort()
		temp_level = sum(t[3:16])/float(14) # 14 elements are left when You remove 3 elemens from the begin and 3 elements from the tail of sorted array
		temp_resistance = self.ConvertResistance(temp_level,2)
		temp = self.ConvertTemp(temp_resistance, 2)
		return temp



