#!/usr/bin/python

import pigpio


class PWMMotor:
	def __init__(self, pi, pinMain = 26, pinControl1 = 19, pinControl2 = 13, pinControl3 = 6, pinControl4 = 5):
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
			self.setControlPWMFrequency(i + 1)
			self.pi.set_PWM_range(self.pinControl[i + 1], 100)
			self.setControlOff(i + 1)
			
	def startMotor(self):
		self.pi.write(self.pinMain, 1)
		
		
	def stopMotor(self):
		self.pi.write(self.pinMain, 0)
		
	def setControlPWMFrequency(self, control, freq = 8000):
		if (control - 1) not in range(4):
			return
		self.pi.set_PWM_frequency(self.pinControl[control],freq)
	
	def getControlPWMFrequency(self, control):
		if (control - 1) not in range(4):
			return -1
		return self.get_PWM_frequency(self.pinControl[control])
	
	# control = 1..4; 
	# level = 0 ..100; 0 - off; 100 - fully on
	def setControlLevel(self, control, level):
		if (control - 1) not in range(4):
			return
			
		if level not in range(101):
			return
		
		self.pi.set_PWM_dutycycle(self.pinControl[control], level)
	
	def setControlOff(self, control):
		if (control - 1) not in range(4):
			return
		
		self.pi.set_PWM_dutycycle(self.pinControl[control], 0)
	
	def getControlLevel(self, control):
		if (control - 1) not in range(4):
			return -1
		return self.pi.get_PWM_dutycycle(self.pinControl[control])
	

	def delete(self):
		self.stopMotor()
		for i in range(4):
			self.setControlOff(i + 1)
		
