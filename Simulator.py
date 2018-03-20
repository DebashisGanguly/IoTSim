import sys
from Device import Device

if __name__ == "__main__" :
	if (len(sys.argv) != 2) :
		raise UserWarning("Usage : python Simulator.py <config_file.xml>" )
	else :
		config = sys.argv[1]

	device = Device(config)

	print(str(device))

	for CommProtocol in device.CommProtocolList:
		CommProtocol.calcNetworkTimings(device.ApplicationPeriod)
		#print(CommProtocol.TUTime)
		#print(CommProtocol.maxCapacity)
		#print(CommProtocol.txTime)
		#print(CommProtocol.rxTime)
		#print(CommProtocol.idleTime)
