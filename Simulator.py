import sys
from Device import Device
from Event import Event
from Workflow import Workflow

if __name__ == "__main__" :
	if (len(sys.argv) != 4) :
		raise UserWarning("Usage: python Simulator.py config.json networking.trace sensing.trace" )
	else :
		config = sys.argv[1]
		neteorkingTrace = sys.argv[2]
		sensingTrace = sys.argv[3]

	device = Device(config)
	curWorkFlowId = '1'
	curWorkFlow = device.Workflows[curWorkFlowId]
	
	netTraceFile = open(networkingTrace,'r')
	sensTraceFile = open(sensingTrace,'r')
	netLine = netTraceFile.readline()
	sensLine = sensTraceFile.readline()
	netTags = netLine.split(' ')
	netTime = long(netTags[0])
	senseTags = sensLine.split(' ')
	sensTime = long(senseTags[0])
	protocolPDRs = {}
	if netTime < sensTime:
		tcur = netTime
		for protocolId in device.Protocols:
			protocolPDRs[protocolId] = float(netTags[int(protocolId)])
	else:
		tcur=sensTime
		for protocolId in device.Protocols:
			protocolPDRs[protocolId] = 1.0
	
	granularity=100000000000000
	sensorTicks={}
	sensorPeriods={}
	for sensor in device.Sensors:
		sensorTicks[sensor] = 0
		if device.Sensors[sensor].SensingPeriod < granularity:
			granularity = device.Sensors[sensor].SensingPeriod
	for sensor in device.Sensors:
		sensorPeriods[sensor] = int(device.Sensors[sensor].SensingPeriod/granularity)
	
	tcur=min(netTime,sensTime)
	
	eventList=[]
	missed = 0
	while netLine or sensLine:
		for sensor in device.Sensors:
			sensorTicks[sensor] = sensorTicks[sensor] + 1
			if sensorTicks[sensor] == sensorPeriods[sensor]:
				sensorTicks[sensor] = 0
				if curWorkFlow.SensorId == sensor:
					#calculate workflow energy
					if sensLine and tcur > int(senseTags[1]):
						sensLine = sensTraceFile.readline()
						if sensLine:
							senseTags = sensLine.split(' ')
					if sensLine:
						if tcur > int(senseTags[1]):
							missed = missed + 1
						else if tcur > int(senseTags[0]):
							#use rules with incident motion to change workflow
						else:
							#use rules with incident still to change workflow
		tcur = tcur + granularity
		while tcur > netTime and netLine:
			for protocolId in device.Protocols:
				protocolPDRs[protocolId] = float(netTags[int(protocolId)])
			netLine = netTraceFile.readline()
			if netLine:
				netTags = netLine.split(' ')		
				netTime = long(netTags[0])
				
				
	print(str(device))


