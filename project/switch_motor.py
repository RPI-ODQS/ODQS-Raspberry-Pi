#!/usr/bin/python

import pigpio


class SwitchMotor:
	def __init__(self, pi, pinMain = 21, pinControl1 = 20, pinControl2 = 16, pinControl3 = 12, pinControl4 = 25):
		self.pi = pi
		self.pinMain = pinMain
		self.pinControl = {}
		self.pinControl[1] = pinControl1
		self.pinControl[2] = pinControl2
		self.pinControl[3] = pinControl3
		self.pinControl[4] = pinControl4
		
		self.pi.set_mode(pinMain, pigpio.OUTPUT) # set GPIO as output
		self.stopMotor()
		
		for i in range(4):
			self.pi.set_mode(self.pinControl[i+1], pigpio.OUTPUT) # set GPIO as output
			self.setControlOff(i + 1)
			
	def startMotor(self):
		self.pi.write(self.pinMain, 1)
		
		
	def stopMotor(self):
		self.pi.write(self.pinMain, 0)
		
		
	# control = 1..4; 
	def setControlOn(self, control):
		if (control - 1) not in range(4):
			return
		
		self.pi.write(self.pinControl[control], 1)

	# control = 1..4; 
	def setControlOff(self, control):
		if (control - 1) not in range(4):
			return
		
		self.pi.write(self.pinControl[control], 0)

	# control = 1..4; 
	def getControlValue(self, control):
		if (control - 1) not in range(4):
			return -1
		return self.pi.read(self.pinControl[control])
	
	def delete(self):
		self.stopMotor()
		for i in range(4):
			self.setControlOff(i + 1)
