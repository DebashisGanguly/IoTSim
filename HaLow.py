import xml.etree.ElementTree as ET
from decimal import Decimal
from NetProtocol import NetProtocol

class HaLow(NetProtocol):
	def __init__(self, **kwargs):
		NetProtocol.__init__(self, **kwargs)
		#protocol specific parameters
		TechnoSpecificParamTree = kwargs.pop('TechnoSpecificParamTree')
		self.SIFS = Decimal(TechnoSpecificParamTree.find('SIFS').text)
		self.DIFS = Decimal(TechnoSpecificParamTree.find('DIFS').text)
		self.Backoff = Decimal(TechnoSpecificParamTree.find('Backoff').text)
		FC = Decimal(TechnoSpecificParamTree.find('FC').text) 
		Duration = Decimal(TechnoSpecificParamTree.find('Duration').text)
		SenderAddress = Decimal(TechnoSpecificParamTree.find('SenderAddress').text) 
		FCS = Decimal(TechnoSpecificParamTree.find('FCS').text)
		Timestamp = Decimal(TechnoSpecificParamTree.find('Timestamp').text) 
		BI = Decimal(TechnoSpecificParamTree.find('BI').text) 
		Capability = Decimal(TechnoSpecificParamTree.find('Capability').text) 
		IEHeader = Decimal(TechnoSpecificParamTree.find('IEHeader').text)
		SSID = Decimal(TechnoSpecificParamTree.find('SSID').text)
		Rates = Decimal(TechnoSpecificParamTree.find('Rates').text)  
		DSParameterSet = Decimal(TechnoSpecificParamTree.find('DSParameterSet').text)
		TIM = Decimal(TechnoSpecificParamTree.find('TIM').text)
		IEBeacons = (IEHeader + SSID) +\
					(IEHeader + Rates) +\
					(IEHeader + DSParameterSet) +\
					(IEHeader + TIM)
		beaconMACFrameSize = FC + Duration + SenderAddress + FCS + Timestamp + BI + Capability + IEBeacons
		# (bits / Mbps -> us) 
		self.beaconTime = (beaconMACFrameSize * 8) / self.PHYRate + self.PHYOverhead
		self.ackTime = self.PHYOverhead

	def ackedTransmissionRxTime(self):
		return (self.ackTime + (self.DIFS + self.Backoff))
		
	def ackedTransmissionIdleTime(self):
		return self.SIFS
	
	def APRxOverhead(self):
		return self.guardInterval + self.beaconTime
	
	def APIdleOverhead(self):
		return 0
