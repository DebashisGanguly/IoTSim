import xml.etree.ElementTree as ET
from NetProtocol import NetProtocol

class BLE(NetProtocol):
	def __init__(self, **kwargs):
		NetProtocol.__init__(self, **kwargs)
		#protocol specific parameters
		TechnoSpecificParamTree = kwargs.pop('TechnoSpecificParamTree')
		self.TIFS = float(TechnoSpecificParamTree.find('TIFS').text)
		LLDataHeader = float(TechnoSpecificParamTree.find('LLDataHeader').text)
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
