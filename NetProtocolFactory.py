from BLE import BLE
from HaLow import HaLow

class NetProtocolFactory:
	def getNetProtocol(type, **kwargs):
		if 'BLE' in type: 
			return BLE(**kwargs)
		if '802.11ah' in type: 
			return HaLow(**kwargs)
		assert 0, "Bad NetProtocol creation: " + type

	getNetProtocol = staticmethod(getNetProtocol)