from NetProtocol import NetProtocol

class HaLow(NetProtocol):
	def __init__(self, **kwargs):
		NetProtocol.__init__(self, **kwargs)
		
		#protocol specific parameters
		ProtocolSpecificParam = kwargs.pop('ProtocolSpecificParam')
		self.SIFS = float(ProtocolSpecificParam['SIFS'])
		self.DIFS = float(ProtocolSpecificParam['DIFS'])
		self.Backoff = float(ProtocolSpecificParam['Backoff'])
		FC = float(ProtocolSpecificParam['FC']) 
		Duration = float(ProtocolSpecificParam['Duration'])
		SenderAddress = float(ProtocolSpecificParam['SenderAddress']) 
		FCS = float(ProtocolSpecificParam['FCS'])
		Timestamp = float(ProtocolSpecificParam['Timestamp']) 
		BI = float(ProtocolSpecificParam['BI']) 
		Capability = float(ProtocolSpecificParam['Capability']) 
		IEHeader = float(ProtocolSpecificParam['IEHeader'])
		SSID = float(ProtocolSpecificParam['SSID'])
		Rates = float(ProtocolSpecificParam['Rates'])  
		DSParameterSet = float(ProtocolSpecificParam['DSParameterSet'])
		TIM = float(ProtocolSpecificParam['TIM'])
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

	def synchroPeriodTimings(self, period):
		output = {	'tx'	: 0,\
					'rx'	: self.APRxOverhead(),\
					'idle'	: self.APIdleOverhead(),\
					'sleep' : period - (self.APRxOverhead() + self.APIdleOverhead()) }
		return output

