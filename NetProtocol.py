from fuzzymath import *

class NetProtocol:
	def __init__(self, **kwargs):
		self.guardInterval = 0
		self.TechnoName = kwargs.pop('TechnoName')
		self.Rx = kwargs.pop('Rx')
		self.Tx = kwargs.pop('Tx')
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
		string += "\n\t\tRx = " + str(self.Rx) + " mW"
		string += "\n\t\tTx = " + str(self.Tx) + " mW"
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

	def detProtocolCapacity(self, ApplicationPeriod, DutyCycle = 1):
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
		
		totalData = (numTotalTransmissions - numNonFullTransmission) * self.MaxPacketSize * 8 + \
				          fullCommPeriodParam['leftOverData'] * numFullCommPeriod +  \
				          lastCommPeriodParam['leftOverData']  #in bits
		
		totalTime = ApplicationPeriod / DutyCycle #in ms 
		
		maxCapacity = totalData / totalTime # bits / ms <=> kbps	
		
		txTime = numFullPackets * self.maxPacketTime() + \
					  numFullCommPeriod * self.dataPacketTime(fullCommPeriodParam['leftOverData']) + \
					  self.dataPacketTime(lastCommPeriodParam['leftOverData'])		 
		
		rxTime = numFullTransmissions * self.ackedTransmissionRxTime() + self.APRxOverhead() * numCommPeriod
		
		idleTime = numFullTransmissions * self.ackedTransmissionIdleTime() + self.APIdleOverhead() * numCommPeriod
		
		output = { 'totalData' : totalData, \
				   'totalTime' : totalTime, \
				   'maxCapacity' : maxCapacity, \
				   'txTime' : txTime, \
				   'rxTime' : rxTime, \
				   'idleTime' : idleTime}
		
		return output

	def detProtocolTimings(self, AmountOfData, ApplicationPeriod, DutyCycle = 1):
		optimalInterval = (ApplicationPeriod / DutyCycle) * pow(10, 3) #in us
		actualInterval = min(optimalInterval, self.SynchroPeriod * pow(10, 3)) #in us	
		MaxApplicationPeriod = min(ApplicationPeriod, actualInterval * pow(10, -3)) #in ms 
		
		numFullCommPeriod = fuzzyFloor(ApplicationPeriod * pow(10, 3) / actualInterval)
		
		fullCommPeriodParam = self.detProtocolCapacity(MaxApplicationPeriod)
		if fullCommPeriodParam['totalData'] == 0:
			print("Amount of data: " + str(AmountOfData) + ", Sensing period: " + str(ApplicationPeriod))
			print("Protocol Name: " + str(self.TechnoName) + ", PDR: " + str(self.PacketDeliveryRatio))
		numMaxAppTransmitPeriod = fuzzyFloor(AmountOfData / fullCommPeriodParam['totalData']) 	
		
		fullCommPeriodParam['sleepTime'] = actualInterval - (fullCommPeriodParam['txTime'] + fullCommPeriodParam['rxTime'] + fullCommPeriodParam['idleTime'])
		
		lastFullPeriodDataToSend = AmountOfData % fullCommPeriodParam['totalData']
		
		if lastFullPeriodDataToSend > 0 :
			numFullTransmittingPeriod = numMaxAppTransmitPeriod + 1	
			numFullDataPackets = fuzzyFloor(lastFullPeriodDataToSend / (self.MaxPacketSize * 8)) 
			leftOverSize = lastFullPeriodDataToSend % (self.MaxPacketSize * 8)
			
			if leftOverSize > 0 :
				numFullTransmission = numFullDataPackets + 1
			else :
				numFullTransmission = numFullDataPackets 
			
			numTotalTransmissions = numFullTransmission * self.PacketDeliveryRatio / 100					
			
			lastFullPeriodTx =  (numFullDataPackets  * self.maxPacketTime() + self.dataPacketTime(leftOverSize)) * self.PacketDeliveryRatio / 100
			lastFullPeriodRx = numTotalTransmissions * self.ackedTransmissionRxTime() + self.APRxOverhead() 
			lastFullPeriodIdle = numTotalTransmissions * self.ackedTransmissionIdleTime() + self.APIdleOverhead()
			lastFullPeriodSleep = actualInterval - (lastFullPeriodTx + lastFullPeriodRx + lastFullPeriodIdle)	
		else : 
			numFullTransmittingPeriod = numMaxAppTransmitPeriod
			lastFullPeriodTx = lastFullPeriodRx = lastFullPeriodIdle = lastFullPeriodSleep = 0
		
		synchroTimings = self.synchroPeriodTimings(actualInterval)																		
		
		if numFullCommPeriod > 0 :
			numFullSleepingPeriod = numFullCommPeriod - numFullTransmittingPeriod
		else :
			numFullSleepingPeriod = 0	
		
		lastPeriodLength = (ApplicationPeriod * pow(10, 3)) % actualInterval
		factor = float(lastPeriodLength) / float(actualInterval)
		
		if (numMaxAppTransmitPeriod == numFullCommPeriod) :
			lastPeriodDataToSend = AmountOfData % fullCommPeriodParam['totalData']
			numFullDataPackets = fuzzyFloor(lastPeriodDataToSend / (self.MaxPacketSize * 8))
			leftOverSize = lastFullPeriodDataToSend % (self.MaxPacketSize * 8)
			
			if leftOverSize > 0 :
				numFullTransmission = numFullDataPackets + 1
			else :
				numFullTransmission = numFullDataPackets
			
			numTotalTransmissions = factor * (numFullTransmission * self.PacketDeliveryRatio / 100)
			
			lastPeriodTx = factor * ((numFullDataPackets * self.maxPacketTime() + self.dataPacketTime(leftOverSize)) * self.PacketDeliveryRatio / 100)
			lastPeriodRx = factor * (numTotalTransmissions * self.ackedTransmissionRxTime() + self.APRxOverhead())
			lastPeriodIdle = factor * (numTotalTransmissions * self.ackedTransmissionIdleTime() + self.APIdleOverhead())
		else :
			lastPeriodTx = factor * synchroTimings['tx'] 
			lastPeriodRx = factor * synchroTimings['rx']
			lastPeriodIdle = factor * synchroTimings['idle']	
		
		lastPeriodSleep = factor * actualInterval - (lastPeriodTx + lastPeriodRx + lastPeriodIdle)
		
		outputs = {}
		
		outputs['timeTxMode'] = (numMaxAppTransmitPeriod * fullCommPeriodParam['txTime'] \
									+ lastFullPeriodTx \
									+ numFullSleepingPeriod * synchroTimings['tx'] \
									+ lastPeriodTx ) / pow(10,6)  # in s
									
		outputs['timeRxMode'] = (numMaxAppTransmitPeriod * fullCommPeriodParam['rxTime'] \
									+ lastFullPeriodRx \
									+ numFullSleepingPeriod * synchroTimings['rx'] \
									+ lastPeriodRx) / pow(10,6)  # in s
									
		outputs['timeIdleMode'] = (numMaxAppTransmitPeriod * fullCommPeriodParam['idleTime'] \
									+ lastFullPeriodIdle \
									+ numFullSleepingPeriod * synchroTimings['idle'] \
									+ lastPeriodIdle ) / pow(10,6)  # in s
									
		outputs['timeSleepMode'] = (numMaxAppTransmitPeriod * fullCommPeriodParam['sleepTime'] \
									+ lastFullPeriodSleep \
									+ numFullSleepingPeriod * synchroTimings['sleep'] \
									+ lastPeriodSleep ) / pow(10,6)  # in s
		
		return outputs



