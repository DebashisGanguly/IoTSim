import sys
from Device import Device
from Workflow import Workflow
from Scheme import Scheme
import math
import json
import plotly

if __name__ == "__main__" :
	if (len(sys.argv) != 4) :
		raise UserWarning("Usage: python Simulator.py config.json networking.trace sensing.trace" )
	else :
		config = sys.argv[1]
		networkingTrace = sys.argv[2]
		sensingTrace = sys.argv[3]

	device = Device(config)
	
	
	netTraceFile = open(networkingTrace,'r')
	sensTraceFile = open(sensingTrace,'r')
	netLine = netTraceFile.readline()
	sensLine = sensTraceFile.readline()
	netTags = netLine.split(' ')
	netTime = int(netTags[0])
	senseTags = sensLine.split(' ')
	sensTime = int(senseTags[0])
	protocolPDRs = {}
	protocolPDRs[0] = 0.0 #For the 'None' protocol
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
	critScore = {}
	consumedEnergy = {}
	schemeEnergies = {}
	
	sensor1 = {}
	sensor1['x'] = []
	sensor1['y'] = []
	sensor1['type'] = 'scatter'
	sensor1['name'] = 'PIR sensor vaue'
	sensor1['mode'] = 'markers'
	
	for SchemeId in device.Schemes:
		curWorkFlowIds[SchemeId] = device.Schemes[SchemeId].DefaultWorkflowId
		curWorkFlows[SchemeId] = device.Workflows[int(curWorkFlowIds[SchemeId])]
		lastBusyTimes[SchemeId] = 0
		prevTimes[SchemeId] = tcur
		consumedEnergy[SchemeId] = 0
		critScore[SchemeId] = 0.0
		schemeEnergies[SchemeId] = {}
		schemeEnergies[SchemeId]['x'] = []
		schemeEnergies[SchemeId]['y'] = []
		schemeEnergies[SchemeId]['type'] = 'scatter'
		schemeEnergies[SchemeId]['name'] = device.Schemes[SchemeId].Name
		schemeEnergies[SchemeId]['mode'] = 'markers+lines'
	missed = 0
	count = 0
	while netLine or sensLine:
		for sensor in device.Sensors:
			sensorTicks[sensor] = sensorTicks[sensor] + 1
			if sensorTicks[sensor] == sensorPeriods[sensor]:
				sensorTicks[sensor] = 0
				for SchemeId in device.Schemes:
					if int(curWorkFlows[SchemeId].SensorId) == sensor:
						energyAndTime = device.calcConsumedEnergy(curWorkFlows[SchemeId], protocolPDRs[int(curWorkFlows[SchemeId].ProtocolId)])
						curEnergy = consumedEnergy[SchemeId]
						if energyAndTime[0] == float("inf"):
							#print("Scheme: " + device.Schemes[SchemeId].Name + " with protocol: " + device.Protocols[device.Workflows[curWorkFlowIds[SchemeId]].ProtocolId].TechnoName + " has PDR = 0. No communication will take place. May miss critical information.")
							schemeSensor = device.Sensors[curWorkFlows[SchemeId].SensorId]
							schemeProcAlgo = device.ProcAlgos[curWorkFlows[SchemeId].ProcAlgoId]
							critScore[SchemeId] = critScore[SchemeId] - schemeSensor.Criticality * schemeProcAlgo.Accuracy * int(senseTags[2])
							#consumedEnergy[SchemeId] = consumedEnergy[SchemeId] + 1000000000
						elif energyAndTime[0] < 0:
							print("Warning: Scheme: " + device.Schemes[SchemeId].Name + " with protocol: " + device.Protocols[device.Workflows[curWorkFlowIds[SchemeId]].ProtocolId].TechnoName + " produced negative energy!")
						else:
							consumedEnergy[SchemeId] = consumedEnergy[SchemeId] + energyAndTime[0] / 1000
						if tcur > prevTimes[SchemeId]:
							consumedEnergy[SchemeId] = consumedEnergy[SchemeId] + (tcur - prevTimes[SchemeId] - lastBusyTimes[SchemeId]) * device.PowerState.Sleep / 1000000
						if 100000 < count and count < 101000:
							schemeEnergies[SchemeId]['x'].append(tcur)
						#if SchemeId == '1' or SchemeId == '6':
						#	print("Scheme: " + device.Schemes[SchemeId].Name + " consumed " + str(energyAndTime[0]) + " busy energy and " + str(consumedEnergy[SchemeId] - curEnergy) + " total energy actually.")
						#	print("Actual sleep time: " + str(tcur - prevTimes[SchemeId] - lastBusyTimes[SchemeId]))
							schemeEnergies[SchemeId]['y'].append(consumedEnergy[SchemeId] - curEnergy)
						prevTimes[SchemeId] = tcur
						lastBusyTimes[SchemeId] = energyAndTime[1]
		tcur = tcur + granularity
		count = count + 1
		if count%5000 == 0:
			print(str(tcur) + "\n")
		while tcur > netTime and netLine:
			for protocolId in device.Protocols:
				protocolPDRs[protocolId] = float(netTags[int(protocolId)])
			netLine = netTraceFile.readline()
			if netLine:
				netTags = netLine.split(' ')		
				netTime = int(netTags[0])
		if sensLine and tcur > int(senseTags[1]):
			sensLine = sensTraceFile.readline()
			if sensLine:
				senseTags = sensLine.split(' ')
		if sensLine:
			if tcur > int(senseTags[1]):
				missed = missed + 1
			elif tcur > int(senseTags[0]):
				sensor1['x'].append(tcur)
				sensor1['y'].append(1)
				for SchemeId in device.Schemes:
					nextWorkFlowId = curWorkFlowIds[SchemeId]
					for rule in device.Schemes[SchemeId].Rules:
						if curWorkFlowIds[SchemeId] in rule.CurrentId and rule.Incident == 'Motion':
							potentialWorkflowIds = rule.NewId
							minWorkflowEnergy = float("inf")
							for potentialWorkflowId in potentialWorkflowIds:
								energyAndTime = device.calcConsumedEnergy(device.Workflows[potentialWorkflowId], protocolPDRs[device.Workflows[int(potentialWorkflowId)].ProtocolId])
								potSensor = device.Sensors[device.Workflows[int(potentialWorkflowId)].SensorId]
								if ((energyAndTime[0] + device.PowerState.Sleep * energyAndTime[2] / 1000) / potSensor.SensingPeriod) < minWorkflowEnergy:
									minWorkflowEnergy = ((energyAndTime[0] + device.PowerState.Sleep * energyAndTime[2] / 1000) / potSensor.SensingPeriod)
									nextWorkFlowId = potentialWorkflowId
					curWorkFlowIds[SchemeId] = nextWorkFlowId
					curWorkFlows[SchemeId] = device.Workflows[int(nextWorkFlowId)]
					#if int(curWorkFlows[SchemeId].SensorId) == 1:
					schemeSensor = device.Sensors[curWorkFlows[SchemeId].SensorId]
					schemeProcAlgo = device.ProcAlgos[curWorkFlows[SchemeId].ProcAlgoId]
					critScore[SchemeId] = critScore[SchemeId] + schemeSensor.Criticality * schemeProcAlgo.Accuracy * int(senseTags[2])
				#use rules with incident motion to change workflow
			else:
				sensor1['x'].append(tcur)
				sensor1['y'].append(0)
				for SchemeId in device.Schemes:
					nextWorkFlowId = curWorkFlowIds[SchemeId]
					for rule in device.Schemes[SchemeId].Rules:
						if curWorkFlowIds[SchemeId] in rule.CurrentId and rule.Incident == 'Still':
							potentialWorkflowIds = rule.NewId
							#if SchemeId == '1' or SchemeId == '6':
							#	print("Scheme: " + device.Schemes[SchemeId].Name + ", Potential Workflows: " + str(potentialWorkflowIds))
							minWorkflowEnergy = float("inf")
							for potentialWorkflowId in potentialWorkflowIds:
								energyAndTime = device.calcConsumedEnergy(device.Workflows[int(potentialWorkflowId)], protocolPDRs[device.Workflows[int(potentialWorkflowId)].ProtocolId])
								potSensor = device.Sensors[device.Workflows[int(potentialWorkflowId)].SensorId]
								#if SchemeId == '1' or SchemeId == '6':
								#	print("Workflow: " + str(potentialWorkflowId) + " will consume " + str(energyAndTime[0]) + " busy energy and " + str(energyAndTime[0] + device.PowerState.Sleep * energyAndTime[2] / 1000) + " total energy.")
								#	print("Calculated sleep time: " + str(energyAndTime[2]) + ", calculated busy time: " + str(energyAndTime[1]) + ", period: " + str(potSensor.SensingPeriod))
								if ((energyAndTime[0] + device.PowerState.Sleep * energyAndTime[2] / 1000) / potSensor.SensingPeriod) < minWorkflowEnergy:
									minWorkflowEnergy = ((energyAndTime[0] + device.PowerState.Sleep * energyAndTime[2] / 1000) / potSensor.SensingPeriod)
									nextWorkFlowId = potentialWorkflowId
					curWorkFlowIds[SchemeId] = nextWorkFlowId
					curWorkFlows[SchemeId] = device.Workflows[int(nextWorkFlowId)]
				#use rules with incident still to change workflow
		
				
	energies = {}
	energies['data'] = []
	energies['layout'] = {'title': 'Energy consumed versus time', 'xaxis': {'title': 'Time'}, 'yaxis': {'title': 'Energy (J)'}}
	
	totalEnergies = {}
	totalEnergies['data'] = []
	totalEnergies['data'].append({})
	totalEnergies['data'][0]['x'] = []
	totalEnergies['data'][0]['y'] = []
	totalEnergies['data'][0]['type'] = 'bar'
	totalEnergies['layout'] = {'title': 'Total Consumed Energy', 'xaxis': {'title': 'Schemes'}, 'yaxis': {'title': 'Energy (J)'}}
	
	criticalities = {}
	criticalities['data'] = []
	criticalities['data'].append({})
	criticalities['data'][0]['x'] = []
	criticalities['data'][0]['y'] = []
	criticalities['data'][0]['type'] = 'bar'
	criticalities['layout'] = {'title': 'Criticality Score', 'xaxis': {'title': 'Schemes'}}
	
	for SchemeId in device.Schemes:
		energies['data'].append(schemeEnergies[SchemeId])
		totalEnergies['data'][0]['x'].append(device.Schemes[SchemeId].Name)
		totalEnergies['data'][0]['y'].append(consumedEnergy[SchemeId])
		criticalities['data'][0]['x'].append(device.Schemes[SchemeId].Name)
		criticalities['data'][0]['y'].append(critScore[SchemeId])
		print("Scheme: " + device.Schemes[SchemeId].Name + "\n")
		print("\tConsumed Energy: " + str(consumedEnergy[SchemeId]) + " kJ\n")
		print("\tCriticality score: " + str(critScore[SchemeId]) + " \n")
	
	energies['data'].append(sensor1)

	with open('plot_energies_med.json', 'w') as fp:
		json.dump(energies, fp)
	plotly.offline.plot(energies, filename = 'energies_med.html')
	with open('plot_totalEnergies_med.json', 'w') as fp:
		json.dump(totalEnergies, fp)
	plotly.offline.plot(totalEnergies, filename = 'totalEnergies_med.html')
	with open('plot_criticalities_med.json', 'w') as fp:
		json.dump(criticalities, fp)
	plotly.offline.plot(criticalities, filename = 'criticalities_med.html')
