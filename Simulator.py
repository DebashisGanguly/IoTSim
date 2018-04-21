import sys
from Device import Device
from Event import Event
from Workflow import Workflow
from Scheme import Scheme

if __name__ == "__main__" :
	if (len(sys.argv) != 4) :
		raise UserWarning("Usage: python Simulator.py config.json networking.trace sensing.trace" )
	else :
		config = sys.argv[1]
		networkingTrace = sys.argv[2]
		sensingTrace = sys.argv[3]

	device = Device(config)
	
#	curWorkFlowId = '1'
#	curWorkFlow = device.Workflows[curWorkFlowId]
	
	netTraceFile = open(networkingTrace,'r')
	sensTraceFile = open(sensingTrace,'r')
	netLine = netTraceFile.readline()
	sensLine = sensTraceFile.readline()
	netTags = netLine.split(' ')
	netTime = int(netTags[0])
	senseTags = sensLine.split(' ')
	sensTime = int(senseTags[0])
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
	curWorkFlows = {}
	curWorkFlowIds = {}
	lastBusyTimes = {}
	prevTimes = {}
	critFails = {}
	consumedEnergy = {}

	for SchemeId in device.Schemes:
		curWorkFlowIds[SchemeId] = device.Schemes[SchemeId].DefaultWorkflowId
		curWorkFlows[SchemeId] = device.Workflows[int(curWorkFlowIds[SchemeId])]
		lastBusyTimes[SchemeId] = 0
		prevTimes[SchemeId] = tcur
		consumedEnergy[SchemeId] = 0
		critFails[SchemeId] = 0
	missed = 0
#	eventList=[]

	while netLine or sensLine:
		for sensor in device.Sensors:
			sensorTicks[sensor] = sensorTicks[sensor] + 1
			if sensorTicks[sensor] == sensorPeriods[sensor]:
				sensorTicks[sensor] = 0
				for SchemeId in device.Schemes:
					if curWorkFlows[SchemeId].SensorId == sensor:
						energyAndTime = device.calcConsumedEnergy(curWorkFlows[SchemeId], protocolPDRs[curWorkFlows[SchemeId].ProtocolId])
						consumedEnergy = consumedEnergy[SchemeId] + energyAndTime[0]
						if tcur > prevTimes[SchemeId]:
							consumedEnergy[SchemeId] = consumedEnergy[SchemeId] + (tcur - prevTimes[SchemeId] - lastBusyTimes[SchemeId]) * device.CommPowerState.Sleep / 1000
						prevTimes[SchemeId] = tcur
						lastBusyTimes[SchemeId] = energyAndTime[1]
				if sensLine and tcur > int(senseTags[1]):
					sensLine = sensTraceFile.readline()
					if sensLine:
						senseTags = sensLine.split(' ')
				if sensLine:
					if tcur > int(senseTags[1]):
						missed = missed + 1
					elif tcur > int(senseTags[0]):
						for SchemeId in device.Schemes:
							nextWorkFlowId = curWorkFlowIds[SchemeId]
							for rule in device.Schemes[SchemeId].Rules:
								if curWorkFlowIds[SchemeId] in rule.CurrentId and rule.Incident == 'Motion':
									potentialWorkflowIds = rule.NewId
									minWorkflowEnergy = math.inf
									for potentialWorkflowId in potentialWorkflowIds:
										energyAndTime = device.calcConsumedEnergy(device.Workflows[potentialWorkflowId], protocolPDRs[device.WorkFlows[int(potentialWorkflowId)].ProtocolId])
										if ((energyAndTime[0] + device.CommPowerState.Sleep * energyAndTime[2] / 1000) / granularity) < minWorkflowEnergy:
											nextWorkFlowId = potentialWorkflowId
							curWorkFlowIds[SchemeId] = nextWorkFlowId
							curWorkFlows[SchemeId] = device.Workflows[int(nextWorkFlowId)]
							if sensLine and tcur >= int(senseTags[0]) and tcur <= int(senseTags[1]) and int(senseTags[2]) == 1:
								if int(curWorkFlows[SchemeId].SensorId) == 1:
									critFails[SchemeId] = critFails[SchemeId] + 1
						#use rules with incident motion to change workflow
					else:
						for SchemeId in device.Schemes:
							nextWorkFlowId = curWorkFlowIds[SchemeId]
							for rule in device.Schemes[SchemeId].Rules:
								if curWorkFlowIds[SchemeId] in rule.CurrentId and rule.Incident == 'Still':
									potentialWorkflowIds = rule.NewId
									minWorkflowEnergy = math.inf
									for potentialWorkflowId in potentialWorkflowIds:
										energyAndTime = device.calcConsumedEnergy(device.Workflows[int(potentialWorkflowId)], protocolPDRs[device.WorkFlows[int(potentialWorkflowId)].ProtocolId])
										if ((energyAndTime[0] + device.CommPowerState.Sleep * energyAndTime[2] / 1000) / granularity) < minWorkflowEnergy:
											nextWorkFlowId = potentialWorkflowId
							curWorkFlowIds[SchemeId] = nextWorkFlowId
							curWorkFlows[SchemeId] = device.Workflows[int(nextWorkFlowId)]
						#use rules with incident still to change workflow
		tcur = tcur + granularity
		while tcur > netTime and netLine:
			for protocolId in device.Protocols:
				protocolPDRs[protocolId] = float(netTags[int(protocolId)])
			netLine = netTraceFile.readline()
			if netLine:
				netTags = netLine.split(' ')		
				netTime = int(netTags[0])
				
				
	print(str(device))


