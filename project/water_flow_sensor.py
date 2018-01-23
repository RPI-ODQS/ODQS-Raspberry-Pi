#!/usr/bin/env python

import pigpio
import time

class WaterFlow:
	def __init__(self, pi, pin = 23):
		self.pin = pin
		self.pi = pi
		
		self.numberOfPress = 0
		self.initialTime = time.time()

		
		self.cb = pi.callback(self.pin)

	def getFlowRate(self):
		flow_frequency = self.cb.tally()
		self.cb.reset_tally()
		
		timeCorrection = ((time.time() - self.initialTime))
		
		self.initialTime = time.time()
		# Pulse frequency (Hz) = 7.5Q, Q is flow rate in L/min. (Results in +/- 3% range)
		litrePerHour = (flow_frequency / timeCorrection * 60 / 7.5); # (Pulse frequency x 60 min) / 7.5 Q = flow rate in L/hour 
		return round(litrePerHour, 2)
	
	def delete(self):
		self.cb.cancel()
