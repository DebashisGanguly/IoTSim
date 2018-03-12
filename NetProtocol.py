class NetProtocol:
	def __init__(self, **kwargs):
		self.TechnoName = kwargs.pop('TechnoName')
		self.MaxPacketSize = kwargs.pop('MaxPacketSize')
		self.PHYRate = kwargs.pop('PHYRate')
		self.PHYOverhead = kwargs.pop('PHYOverhead')
		self.MACOverhead = kwargs.pop('MACOverhead')
		self.IPv6Overhead = kwargs.pop('IPv6Overhead')
		self.SynchroPeriod = kwargs.pop('SynchroPeriod')
		self.ClockAccuracy = kwargs.pop('ClockAccuracy')
		self.PacketDeliveryRatio = kwargs.pop('PacketDeliveryRatio')

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

