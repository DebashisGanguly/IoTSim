import sys
from Device import Device
from Event import Event

if __name__ == "__main__" :
	if (len(sys.argv) != 4) :
		raise UserWarning("Usage: python Simulator.py config.json networking.trace sensing.trace" )
	else :
		config = sys.argv[1]
		neteorkingTrace = sys.argv[2]
		sensingTrace = sys.argv[3]

	device = Device(config)

	print(str(device))


