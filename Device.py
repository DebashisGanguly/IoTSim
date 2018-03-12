import xml.etree.ElementTree as ET
from decimal import Decimal
from Battery import Battery
from CommPowerState import CommPowerState
from NetProtocol import NetProtocol
from NetProtocolFactory import NetProtocolFactory

class Device:
	def __repr__(self):
		string = "\nConfiguration Items:\n"
		string += "\n\tApplication Period = " + str(self.ApplicationPeriod) + " ms"
		string += "\n\tApplication Data Size = " + str(self.ApplicationDataSize) + " kB"
		string += "\n\tGranularity = " + str(self.Granularity) + " s"
		string += str(self.Battery)
		string += "\n\n\tCommunication Protocols:"
		for CommProtocol in self.CommProtocolList:
			string += str(CommProtocol)
		return string

	def __init__(self, config):
		ConfigTree = ET.parse('config.xml')
		Root = ConfigTree.getroot()
		self.ApplicationPeriod = Decimal(Root.find('ApplicationPeriod').text)
		self.ApplicationDataSize = Decimal(Root.find('ApplicationDataSize').text)
		self.Granularity = Decimal(Root.find('Granularity').text)
		BatterySubTree = Root.find('Battery')
		InitialEnergy = Decimal(BatterySubTree.find('InitialEnergy').text)
		BatteryLeakage = Decimal(BatterySubTree.find('BatteryLeakage').text)
		CutOffThreshold = Decimal(BatterySubTree.find('CutOffThreshold').text)
		self.Battery = Battery(InitialEnergy, BatteryLeakage, CutOffThreshold)
		CommProtocolSubTree = Root.find('CommProtocol')
		self.CommProtocolList = []
		for Techno in CommProtocolSubTree.findall('Techno'):
			TechnoName = Techno.get('Name')
			MaxPacketSize = Decimal(Techno.find('MaxPacketSize').text)
			PHYRate = Decimal(Techno.find('PHYRate').text)
			PHYOverhead = Decimal(Techno.find('PHYOverhead').text)
			MACOverhead = Decimal(Techno.find('MACOverhead').text)
			IPv6Overhead = Decimal(Techno.find('IPv6Overhead').text)
			SynchroPeriod = Decimal(Techno.find('SynchroPeriod').text)
			ClockAccuracy = Decimal(Techno.find('ClockAccuracy').text)
			PacketDeliveryRatio = Decimal(Techno.find('PacketDeliveryRatio').text)
			PowerConsumption = Techno.find('PowerConsumption')
			HWName = PowerConsumption.get('HWName')
			Rx = Decimal(PowerConsumption.find('Rx').text)
			Tx = Decimal(PowerConsumption.find('Tx').text)
			CPUIdle = Decimal(PowerConsumption.find('CPUIdle').text)
			Sleep = Decimal(PowerConsumption.find('Sleep').text)
			CommPowerStateObj = CommPowerState(HWName, Rx, Tx, CPUIdle, Sleep)
			NetProtocolObj = NetProtocolFactory.getNetProtocol(TechnoName, TechnoName = TechnoName, MaxPacketSize = MaxPacketSize, PHYRate = PHYRate, PHYOverhead = PHYOverhead, MACOverhead = MACOverhead, IPv6Overhead = IPv6Overhead, SynchroPeriod = SynchroPeriod, ClockAccuracy = ClockAccuracy, PacketDeliveryRatio = PacketDeliveryRatio, CommPowerState = CommPowerStateObj)
			self.CommProtocolList.append(NetProtocolObj)
