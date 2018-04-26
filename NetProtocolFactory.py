from BLE import BLE
from WiFi import WiFi

class NetProtocolFactory:
	def getNetProtocol(type, **kwargs):
		if 'BLE' in type: 
			return BLE(**kwargs)
		if '802.11' in type: 
			return WiFi(**kwargs)
		assert 0, "Bad NetProtocol creation: " + type

	getNetProtocol = staticmethod(getNetProtocol)
