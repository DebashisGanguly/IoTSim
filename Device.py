import xml.etree.ElementTree as ET
from Queue import Queue
from Battery import Battery
from CommPowerState import CommPowerState
from NetProtocol import NetProtocol
from NetProtocolFactory import NetProtocolFactory
from Event import Event

class Device:
	def __repr__(self):
		string = "\nConfiguration Items:\n"
		string += "\n\tApplication Period = " + str(self.ApplicationPeriod) + " ms"
		string += "\n\tApplication Data Size = " + str(self.ApplicationDataSize) + " kB"
		string += "\n\tGranularity = " + str(self.Granularity) + " s"
		string += str(self.Battery)
		string += str(self.CommPowerState)
		string += "\n\n\tCommunication Protocols:"
		for CommProtocol in self.CommProtocolList:
			string += str(CommProtocol)
		string += "\nDevice Lifetime Events:\n"
		for TraceEvent in list(self.EventQueue.queue):
			string += str(TraceEvent)
		return string

	def __init__(self, config):
		self.Lifetime = 0
		ConfigTree = ET.parse('config.xml')
		Root = ConfigTree.getroot()
		self.ApplicationPeriod = float(Root.find('ApplicationPeriod').text)
		self.ApplicationDataSize = float(Root.find('ApplicationDataSize').text)
		self.Granularity = float(Root.find('Granularity').text)
		BatterySubTree = Root.find('Battery')
		InitialEnergy = float(BatterySubTree.find('InitialEnergy').text)
		BatteryLeakage = float(BatterySubTree.find('BatteryLeakage').text)
		CutOffThreshold = float(BatterySubTree.find('CutOffThreshold').text)
		self.Battery = Battery(InitialEnergy, BatteryLeakage, CutOffThreshold, self.ApplicationPeriod)
		PowerConsumption = Root.find('PowerConsumption')
		HWName = PowerConsumption.get('HWName')
		Rx = float(PowerConsumption.find('Rx').text)
		Tx = float(PowerConsumption.find('Tx').text)
		CPUIdle = float(PowerConsumption.find('CPUIdle').text)
		Sleep = float(PowerConsumption.find('Sleep').text)
		self.CommPowerState = CommPowerState(HWName, Rx, Tx, CPUIdle, Sleep)
		CommProtocolSubTree = Root.find('CommProtocol')
		self.CommProtocolList = []
		for Techno in CommProtocolSubTree.findall('Techno'):
			TechnoName = Techno.get('Name')
			MaxPacketSize = float(Techno.find('MaxPacketSize').text)
			PHYRate = float(Techno.find('PHYRate').text)
			PHYOverhead = float(Techno.find('PHYOverhead').text)
			MACOverhead = float(Techno.find('MACOverhead').text)
			IPv6Overhead = float(Techno.find('IPv6Overhead').text)
			SynchroPeriod = float(Techno.find('SynchroPeriod').text)
			ClockAccuracy = float(Techno.find('ClockAccuracy').text)
			PacketDeliveryRatio = float(Techno.find('PacketDeliveryRatio').text)
			TechnoSpecificParamTree = Techno.find('TechnoSpecificParam')
			NetProtocolObj = NetProtocolFactory.getNetProtocol(TechnoName, TechnoName = TechnoName, MaxPacketSize = MaxPacketSize, PHYRate = PHYRate, PHYOverhead = PHYOverhead, MACOverhead = MACOverhead, IPv6Overhead = IPv6Overhead, SynchroPeriod = SynchroPeriod, ClockAccuracy = ClockAccuracy, PacketDeliveryRatio = PacketDeliveryRatio, TechnoSpecificParamTree = TechnoSpecificParamTree)
			self.CommProtocolList.append(NetProtocolObj)
		self.TraceFile = Root.find('TraceFile').text
		self.populateLifetimeEvents(self.TraceFile)

	def populateLifetimeEvents(self, TraceFile):
		self.EventQueue = Queue()
		ConfigTree = ET.parse(TraceFile)
		Root = ConfigTree.getroot()
		for TraceEvent in Root.findall('Event'):
			Type = TraceEvent.get('Type')
			TimeOffset = float(TraceEvent.find('TimeOffset').text)
			EventParamTree = TraceEvent.find('EventParameter')
			NewEvent = Event(Type, TimeOffset, EventParamTree)
			self.EventQueue.put(NewEvent)

	def calcConsumedEnergy(self):
		minCommEnergyExpense = -1
		for CommProtocol in self.CommProtocolList:
			protocolTimings = CommProtocol.detProtocolTimings(float(self.ApplicationDataSize * 8 * pow(10,3)), self.ApplicationPeriod)
			CommEnergyExpense =   protocolTimings['timeTxMode']    * self.CommPowerState.Tx \
								+ protocolTimings['timeRxMode']    * self.CommPowerState.Rx \
								+ protocolTimings['timeIdleMode']  * self.CommPowerState.CPUIdle \
								+ protocolTimings['timeSleepMode'] * self.CommPowerState.Sleep # in mJ
			if (minCommEnergyExpense == -1) or (CommEnergyExpense < minCommEnergyExpense):
				minCommEnergyExpense = minCommEnergyExpense
				bestCommProtocol = CommProtocol.TechnoName
		return minCommEnergyExpense

	def incLifetime(self):
		self.Lifetime += self.ApplicationPeriod
