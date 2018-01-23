#!/usr/bin/env python

import pigpio

class Button:
	def __init__(self, pi, pin):
		self.pin = pin
		self.pi = pi
		
		
	def isDown(self):
		if (self.pi.read(self.pin) == 1):
			return True
		else:
			return False
		
	def isUp(self):
		if (self.pi.read(self.pin) == 0):
			return True
		else:
			return False

