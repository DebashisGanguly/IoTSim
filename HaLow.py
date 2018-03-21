import xml.etree.ElementTree as ET
from NetProtocol import NetProtocol

class HaLow(NetProtocol):
	def __init__(self, **kwargs):
		NetProtocol.__init__(self, **kwargs)
		#protocol specific parameters
		TechnoSpecificParamTree = kwargs.pop('TechnoSpecificParamTree')
		self.SIFS = float(TechnoSpecificParamTree.find('SIFS').text)
		self.DIFS = float(TechnoSpecificParamTree.find('DIFS').text)
		self.Backoff = float(TechnoSpecificParamTree.find('Backoff').text)
		FC = float(TechnoSpecificParamTree.find('FC').text) 
		Duration = float(TechnoSpecificParamTree.find('Duration').text)
		SenderAddress = float(TechnoSpecificParamTree.find('SenderAddress').text) 
		FCS = float(TechnoSpecificParamTree.find('FCS').text)
		Timestamp = float(TechnoSpecificParamTree.find('Timestamp').text) 
		BI = float(TechnoSpecificParamTree.find('BI').text) 
		Capability = float(TechnoSpecificParamTree.find('Capability').text) 
		IEHeader = float(TechnoSpecificParamTree.find('IEHeader').text)
		SSID = float(TechnoSpecificParamTree.find('SSID').text)
		Rates = float(TechnoSpecificParamTree.find('Rates').text)  
		DSParameterSet = float(TechnoSpecificParamTree.find('DSParameterSet').text)
		TIM = float(TechnoSpecificParamTree.find('TIM').text)
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
