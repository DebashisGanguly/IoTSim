import sys
from Device import Device

if __name__ == "__main__" :
	if (len(sys.argv) != 2) :
		raise UserWarning("Usage: python Simulator.py config.json" )
	else :
		config = sys.argv[1]

	device = Device(config)

	print(str(device))


