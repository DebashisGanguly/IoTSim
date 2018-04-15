from NetProtocol import NetProtocol

class BLE(NetProtocol):
	def __init__(self, **kwargs):
		NetProtocol.__init__(self, **kwargs)
		
		#protocol specific parameters
		ProtocolSpecificParam = kwargs.pop('ProtocolSpecificParam')
		self.TIFS = float(ProtocolSpecificParam['TIFS'])
		LLDataHeader = float(ProtocolSpecificParam['LLDataHeader'])
		self.ackTime = (self.MACOverhead - LLDataHeader) / 	self.PHYRate + self.PHYOverhead	
		self.pollTime = self.MACOverhead / self.PHYRate + self.PHYOverhead

	def ackedTransmissionRxTime(self):
		return self.ackTime
		
	def ackedTransmissionIdleTime(self):
		return 2 * self.TIFS
	
	def APRxOverhead(self):
		return self.guardInterval + self.pollTime
	
	def APIdleOverhead(self):
		return self.TIFS

	def synchroPeriodTimings(self, period):
		output = {  'tx'	: self.ackTime,\
					'rx'	: self.APRxOverhead(),\
					'idle'	: self.APIdleOverhead() + self.TIFS,\
					'sleep' : period - (self.ackTime + self.APRxOverhead() + self.APIdleOverhead() + self.TIFS)}
		return output
