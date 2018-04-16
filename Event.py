class Event:
	def __init__(self, Type, TimeOffset, EventSepecificParam):
		self.Type = Type
		self.TimeOffset = TimeOffset
		
		self.param = {}

		if self.Type == 'Networking':
			self.param['ProtocolId'] = EventSepecificParam['ProtocolId']
			self.param['PacketDeliveryRatio'] = float(EventSepecificParam['PacketDeliveryRatio'])

		if self.Type == 'Sensing':
			self.param['SensorId'] = EventSepecificParam['SensorId']
			self.param['Incident'] = float(EventSepecificParam['Incident'])


	def __repr__(self):
		string = '\n\tEvent of type ' + self.Type + ' occured at time ' + str(self.TimeOffset) + ' ms from start;'
		string += '\n\t\tEvent parameters:'
		for key, value in self.param.iteritems():
			string += '\n\t\t\t' + key + ': ' + str(value)
		return string