import xml.etree.ElementTree as ET

class Event:
	def __init__(self, Type, TimeOffset, EventParamTree):
		self.Type = Type
		self.TimeOffset = TimeOffset
		self.param = {}
		if self.Type == 'Network':
			self.param['Name'] = EventParamTree.find('Name').text
			self.param['ClockAccuracy'] = float(EventParamTree.find('ClockAccuracy').text)
			self.param['PacketDeliveryRatio'] = float(EventParamTree.find('PacketDeliveryRatio').text)

	def __repr__(self):
		string = '\n\tEvent of type ' + self.Type + ' occured at time ' + str(self.TimeOffset) + ' ms from start;'
		string += '\n\t\tEvent parameters:'
		for key, value in self.param.iteritems():
			string += '\n\t\t\t' + key + ': ' + str(value)
		return string