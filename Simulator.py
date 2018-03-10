import xml.etree.ElementTree as ET
from decimal import Decimal

ConfigTree = ET.parse('config.xml')

Root = ConfigTree.getroot()

ApplicationPeriod = Decimal(Root.find('ApplicationPeriod').text)
ApplicationDataSize = Decimal(Root.find('ApplicationDataSize').text)
Granularity = Decimal(Root.find('Granularity').text)

print "\nConfiguration Items:\n"

print "\tApplication Period = " + str(ApplicationPeriod) + " ms"
print "\tApplication Data Size = " + str(ApplicationDataSize) + " kB"
print "\tGranularity = " + str(Granularity) + " s"

Battery = Root.find('Battery')

InitialEnergy = Decimal(Battery.find('InitialEnergy').text)
BatteryLeakage = Decimal(Battery.find('BatteryLeakage').text)
CutOffThreshold = Decimal(Battery.find('CutOffThreshold').text)

print "\n\tBattery:\n"

print "\t\tInitial Energy = " + str(InitialEnergy) + " mJ"
print "\t\tBattery Leakage = " + str(BatteryLeakage) + " %"
print "\t\tCut Off Threshold = " + str(CutOffThreshold) + " %"

CommProtocol = Root.find('CommProtocol')

print "\n\tCommunication Protocol:\n"

for Techno in CommProtocol.findall('Techno'):
	TechnoName = Techno.get('Name')
	MaxPacketSize = Decimal(Techno.find('MaxPacketSize').text)
	PHYRate = Decimal(Techno.find('PHYRate').text)
	PHYOverhead = Decimal(Techno.find('PHYOverhead').text)
	MACOverhead = Decimal(Techno.find('MACOverhead').text)
	IPv6Overhead = Decimal(Techno.find('IPv6Overhead').text)
	SynchroPeriod = Decimal(Techno.find('SynchroPeriod').text)
	ClockAccuracy = Decimal(Techno.find('ClockAccuracy').text)
	PacketDeliveryRatio = Decimal(Techno.find('PacketDeliveryRatio').text)
	print "\n\t\tTechnology Details:\n"
	print "\t\t\tName = " + TechnoName
	print "\t\t\tMax Packet Size = " + str(MaxPacketSize) + " bytes"
	print "\t\t\tPHY Rate = " + str(PHYRate) + " mbps"
	print "\t\t\tPHY Overhead = " + str(PHYOverhead) + " us"
	print "\t\t\tMAC Overhead = " + str(MACOverhead) + " bits"
	print "\t\t\tIPv6 Overhead = " + str(IPv6Overhead) + " bits"
	print "\t\t\tSynchronization Period = " + str(SynchroPeriod) + " ms"
	print "\t\t\tClock Accuracy = " + str(ClockAccuracy) + " ppm"
	print "\t\t\tPacket Delivery Ratio = " + str(PacketDeliveryRatio) + " %"
	PowerConsumption = Techno.find('PowerConsumption')
	HWName = PowerConsumption.get('HWName')
	Rx = Decimal(PowerConsumption.find('Rx').text)
	Tx = Decimal(PowerConsumption.find('Tx').text)
	CPUIdle = Decimal(PowerConsumption.find('CPUIdle').text)
	Sleep = Decimal(PowerConsumption.find('Sleep').text)
	print "\n\t\t\tPower Consumption:\n"
	print "\t\t\t\tHardware Name = " + HWName
	print "\t\t\t\tRx = " + str(Rx) + " mW"
	print "\t\t\t\tTx = " + str(Tx) + " mW"
	print "\t\t\t\tCPU Idle = " + str(CPUIdle) + " mW"
	print "\t\t\t\tSleep = " + str(Sleep) + " mW"
