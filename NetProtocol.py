from fuzzymath import *

class NetProtocol:
	def __init__(self, **kwargs):
		self.guardInterval = 0
		self.TechnoName = kwargs.pop('TechnoName')
		self.MaxPacketSize = kwargs.pop('MaxPacketSize')
		self.PHYRate = kwargs.pop('PHYRate')
		self.PHYOverhead = kwargs.pop('PHYOverhead')
		self.MACOverhead = kwargs.pop('MACOverhead')
		self.IPv6Overhead = kwargs.pop('IPv6Overhead')
		self.SynchroPeriod = kwargs.pop('SynchroPeriod')
		self.ClockAccuracy = kwargs.pop('ClockAccuracy')
		self.PacketDeliveryRatio = kwargs.pop('PacketDeliveryRatio')
		#calculate derived attributes
		self.totalPacketOverhead = (self.IPv6Overhead + self.MACOverhead) / self.PHYRate  + self.PHYOverhead

	def __repr__(self):
		string = "\n\n\t\tTechnology Details:\n"
		string += "\n\t\t\tName = " + self.TechnoName
		string += "\n\t\t\tMax Packet Size = " + str(self.MaxPacketSize) + " bytes"
		string += "\n\t\t\tPHY Rate = " + str(self.PHYRate) + " mbps"
		string += "\n\t\t\tPHY Overhead = " + str(self.PHYOverhead) + " us"
		string += "\n\t\t\tMAC Overhead = " + str(self.MACOverhead) + " bits"
		string += "\n\t\t\tIPv6 Overhead = " + str(self.IPv6Overhead) + " bits"
		string += "\n\t\t\tSynchronization Period = " + str(self.SynchroPeriod) + " ms"
		string += "\n\t\t\tClock Accuracy = " + str(self.ClockAccuracy) + " ppm"
		string += "\n\t\t\tPacket Delivery Ratio = " + str(self.PacketDeliveryRatio) + " %"
		return string

	def ackedTransmissionIdleTime(self):
		raise NotImplementedError
	
	def ackedTransmissionRxTime(self):
		raise NotImplementedError

	def APRxOverhead(self):
		raise NotImplementedError
		
	def APIdleOverhead(self):
		raise NotImplementedError

	def APOverhead(self):
		return (self.APRxOverhead() + self.APIdleOverhead())

	def dataPacketTime(self, dataSize): # in us
		if ( dataSize != 0 and dataSize <= self.MaxPacketSize * 8) :
			return dataSize / self.PHYRate + self.totalPacketOverhead
		elif dataSize == 0 :
			return 0
		else : 
			raise ValueError('The data packet exceeds maximum packet size!')

	def maxPacketTime(self):
		return self.dataPacketTime(self.MaxPacketSize * 8)

	def ackedTransmissionOverhead(self): #return time in us
		return self.ackedTransmissionRxTime() + self.ackedTransmissionIdleTime()

	def ackTransmissionTime(self, dataSize): 
		return self.dataPacketTime(dataSize) + self.ackedTransmissionOverhead()

	def calcNumFullPacketAndLeftOverData(self, commPeriod): #commPeriod in us
		numFullPacket = leftOverData = 0
		if (commPeriod > 0) : 
			fullAckTransmissionTime = self.ackTransmissionTime(self.MaxPacketSize * 8)
			numFullPacket = fuzzyFloor((commPeriod - self.APOverhead()) / fullAckTransmissionTime)
			leftOverTime = ((commPeriod - self.APOverhead()) % fullAckTransmissionTime) - self.totalPacketOverhead - self.ackedTransmissionOverhead()
			if (leftOverTime > 0) :
				leftOverData =  fuzzyFloor(leftOverTime * self.PHYRate) 
			else : 
				leftOverData =  0 
		output =  { 'numFullPacket' : numFullPacket,\
				    'leftOverData'  : leftOverData}
		return output 

	def calcNetworkTimings(self, ApplicationPeriod, DutyCycle = 1):
		commPeriod = min(ApplicationPeriod, self.SynchroPeriod) #in ms
		numFullCommPeriod = fuzzyFloor(ApplicationPeriod / commPeriod) #number of full communication period is minimum of time to synchronize and time to send application data
		fullCommPeriodParam = self.calcNumFullPacketAndLeftOverData(commPeriod * pow(10, 3)) #get communication parameters per communication period (superframe/data event/Beacon interval)
		lastCommPeriod = ApplicationPeriod % commPeriod
		if (lastCommPeriod > 0) : 
			numCommPeriod = numFullCommPeriod + 1
		else:
			numCommPeriod = numFullCommPeriod
		lastCommPeriodParam = self.calcNumFullPacketAndLeftOverData(lastCommPeriod * pow(10,3))
		numFullPackets = fullCommPeriodParam['numFullPacket'] * numFullCommPeriod + lastCommPeriodParam['numFullPacket'] 
		numFullTransmissions = numFullPackets
		if fullCommPeriodParam['leftOverData'] > 0 :
			numFullTransmissions += 1 	
		if lastCommPeriodParam['leftOverData'] > 0 :
			numFullTransmissions += 1	
		numTotalTransmissions = numFullTransmissions * self.PacketDeliveryRatio / 100
		numNonFullTransmission = 0			
		if fullCommPeriodParam['leftOverData'] > 0 :
			numNonFullTransmission += 1
		if lastCommPeriodParam['leftOverData'] > 0 :
			numNonFullTransmission += 1
		self.TUDataSize = (numTotalTransmissions - numNonFullTransmission) * self.MaxPacketSize * 8 + \
				          fullCommPeriodParam['leftOverData'] * numFullCommPeriod +  \
				          lastCommPeriodParam['leftOverData']  #in bits
		self.TUTime = ApplicationPeriod / DutyCycle #in ms 
		self.maxCapacity = self.TUDataSize / self.TUTime # bits / ms <=> kbps	
		self.txTime = numFullPackets * self.maxPacketTime() + \
					  numFullCommPeriod * self.dataPacketTime(fullCommPeriodParam['leftOverData']) + \
					  self.dataPacketTime(lastCommPeriodParam['leftOverData'])		 
		self.rxTime = numFullTransmissions * self.ackedTransmissionRxTime() + self.APRxOverhead() * numCommPeriod
		self.idleTime = numFullTransmissions * self.ackedTransmissionIdleTime() + self.APIdleOverhead() * numCommPeriod


	
