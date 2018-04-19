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
	netTraceFile=open(networkingTrace,'r')
	sensTraceFile=open(sensingTrace,'r')
	netLine=netTraceFile.readline()
	sensLine=sensTraceFile.readline()
	netTime=0
	sensTime=0
	eventList=[]
	while netLine or sensLine:
		if netLine:
			netTags=netLine.split(' ')
			netTime=long(netTags[0])
		if sensLine:
			senseTags=sensLine.split(' ')
			sensTime=long(senseTags[0])
		if sensTime < netTime:
			x=Event('Sensing)
	print(str(device))


