from CommPowerState import CommPowerState
from Sensor import Sensor
from ProcAlgo import ProcAlgo
from NetProtocol import NetProtocol
from NetProtocolFactory import NetProtocolFactory
from Workflow import Workflow
from Rule import Rule
import json
import math

class Device:
	def __repr__(self):
		string = "\nConfiguration Items:"

		string += str(self.CommPowerState)

		string += "\n\n\tSensors:\n"

		for SensorVal in self.Sensors.values():
			string += str(SensorVal)

		string += "\n\n\tProcessing Algorithms:\n"

		for ProcAlgoVal in self.ProcAlgos.values():
			string += str(ProcAlgoVal)

		string += "\n\n\tCommunication Protocols:\n"

		for ProtocolVal in self.Protocols.values():
			string += str(ProtocolVal)

		string += "\n\n\tDevice Context:\n"

		for WorkflowVal in self.Workflows.values():
			string += str(WorkflowVal)

		string += "\n\n\tIf-this-then-that Rules:\n"

		for RuleVal in self.Rules.values():
			string += str(RuleVal)

		return string

	def __init__(self, config):
		fileData = open(config, 'r').read()

		json_data = json.loads(fileData)

		configItems = json_data['Config']

		powerConsumptionItem = configItems['PowerConsumption']

		HWName = powerConsumptionItem['HWName']
		Rx = float(powerConsumptionItem['Rx'])
		Tx = float(powerConsumptionItem['Tx'])
		CPUIdle = float(powerConsumptionItem['CPUIdle'])
		CPUActive = float(powerConsumptionItem['CPUActive'])
		Sleep = float(powerConsumptionItem['Sleep'])

		self.CommPowerState = CommPowerState(HWName, Rx, Tx, CPUIdle, CPUActive, Sleep)

		sensingItem = configItems['Sensing']

		self.Sensors = {}

		for sensorItem in sensingItem['Sensor']:
			SensorId = int(sensorItem['Id'])
			SensorName = sensorItem['Name']
			SensingPeriod = float(sensorItem['SensingPeriod'])
			DataRate = float(sensorItem['DataRate'])
			AcquireTime = float(sensorItem['AcquireTime'])
			StaticPower = float(sensorItem['StaticPower'])
			DynamicPower = float(sensorItem['DynamicPower'])

			SensorObj = Sensor(SensorName, SensingPeriod, DataRate, AcquireTime, StaticPower, DynamicPower)
			self.Sensors[SensorId] = SensorObj

		processingItem = configItems['Processing']

		self.ProcAlgos = {}

		for procAlgoItem in processingItem['ProcAlgo']:
			ProcAlgoId = int(procAlgoItem['Id'])
			ProcAlgoName = procAlgoItem['Name']
			ProcTimePerBit = float(procAlgoItem['ProcTimePerBit'])

			ProcAlgoObj = ProcAlgo(ProcAlgoName, ProcTimePerBit)
			self.ProcAlgos[ProcAlgoId] = ProcAlgoObj

		networkingItem = configItems['Networking']

		self.Protocols = {}

		for protocolItem in networkingItem['Protocol']:
			ProtocolId = int(protocolItem['Id'])
			ProtocolName = protocolItem['Name']
			MaxPacketSize = float(protocolItem['MaxPacketSize'])
			PHYRate = float(protocolItem['PHYRate'])
			PHYOverhead = float(protocolItem['PHYOverhead'])
			MACOverhead = float(protocolItem['MACOverhead'])
			IPv6Overhead = float(protocolItem['IPv6Overhead'])
			SynchroPeriod = float(protocolItem['SynchroPeriod'])
			ClockAccuracy = float(protocolItem['ClockAccuracy'])
			PacketDeliveryRatio = float(protocolItem['PacketDeliveryRatio'])
			ProtocolSpecificParam = protocolItem['ProtocolSpecificParam']

			NetProtocolObj = NetProtocolFactory.getNetProtocol(ProtocolName, TechnoName = ProtocolName, MaxPacketSize = MaxPacketSize, PHYRate = PHYRate, PHYOverhead = PHYOverhead, MACOverhead = MACOverhead, IPv6Overhead = IPv6Overhead, SynchroPeriod = SynchroPeriod, ClockAccuracy = ClockAccuracy, PacketDeliveryRatio = PacketDeliveryRatio, ProtocolSpecificParam = ProtocolSpecificParam)
			self.Protocols[ProtocolId] = NetProtocolObj

		contextItem = configItems['Context']

		self.Workflows = {}

		for workflowItem in contextItem['Workflow']:
			WorkflowId = int(workflowItem['Id'])

			if workflowItem['SensorId'] == 'None':
				SensorId = 0
			elif workflowItem['SensorId'] == 'Any':
				SensorId = -1
			else:
				SensorId = workflowItem['SensorId']

			if workflowItem['ProcAlgoId'] == 'None':
				ProcAlgoId = 0
			elif workflowItem['ProcAlgoId'] == 'Any':
				ProcAlgoId = -1
			else:	
				ProcAlgoId = workflowItem['ProcAlgoId']

			if workflowItem['ProtocolId'] == 'None':
				ProtocolId = 0
			elif workflowItem['ProtocolId'] == 'Any':
				ProtocolId = -1
			else:
				ProtocolId = workflowItem['ProtocolId']

			WorkflowObj = Workflow(SensorId, ProcAlgoId, ProtocolId)
			self.Workflows[WorkflowId] = WorkflowObj

		IFTTTItem = configItems['IFTTT']

		self.Rules = {}

		for ruleItem in IFTTTItem['Rule']:
			RuleId = int(ruleItem['Id'])

			ifItem = ruleItem['If']
			EventType = ifItem['EventType']
			CurId = list(map(int, ifItem['CurId'].split(',')))
			Incident = ifItem['Incident']

			thenItem = ruleItem['Then']
			Action = thenItem['Action']
			NewId = list(map(int, thenItem['NewId'].split(',')))

			RuleObj = Rule(EventType, CurId, Incident, Action, NewId)
			self.Rules[RuleId] = RuleObj

	def calcConsumedEnergy(self, workflow, pdr):
		#minCommEnergyExpense = -1
		ProtocolId = workflow['ProtocolId']
		SensorId = workflow['SensorId']
		ProcAlgoId = workflow['ProcAlgoId']
		sensor = self.Sensors[SensorId]
		procAlgo = self.ProcAlgos[ProcAlgoId]
		ApplicationDataSize = sensor.AcquireTime * sensor.DataRate / (8 * 1000)
		procTime = 8 * ApplicationDataSize / procAlgo.ProcTimePerBit
		CommEnergyExpense = 0
		busyTime = procTime + sensor.AcquireTime
		sleepTime = sensor.SensingPeriod - busyTime
		if ProtocolId != 0 or ProtocolId != -1:
			CommProtocol = self.Protocols[ProtocolId]
			CommProtocol.PacketDeliveryRatio = 100 * pdr
		#for CommProtocol in self.CommProtocolList:
			protocolTimings = CommProtocol.detProtocolTimings(float(ApplicationDataSize * 8), sensor.SensingPeriod)
			CommEnergyExpense =   protocolTimings['timeTxMode']    * self.CommPowerState.Tx \
								+ protocolTimings['timeRxMode']    * self.CommPowerState.Rx \
								+ protocolTimings['timeIdleMode']  * self.CommPowerState.CPUIdle
			sleepTime = protocolTimings['timeSleepMode'] - busyTime
			busyTime = busyTime + (protocolTimings['timeTxMode'] + protocolTimings['timeRxMode'] + protocolTimings['timeIdleMode']) / 1000
		if busyTime > sensor.SensingPeriod:
			print('Cannot perform all operations (sensing, processing and comm) within sensing period. Setting energy consumption to max value.\n')
			print('Protocol: ' + CommProtocol.TechnoName + ', Sensor: ' + sensor.Name + ', ProcAlgo: ' + procAlgo.Name + '\n')
			CommEnergyExpense = math.inf
		else:
			CommEnergyExpense = CommEnergyExpense + \
								((sensor.AcquireTime + procTime) * self.CommPowerState.CPUActive + sensor.AcquireTime * (sensor.StaticPower + sensor.DynamicPower)) / 1000
		retList = []
		retList.append(CommEnergyExpense)
		retList.append(busyTime)
		retList.append(sleepTime)
			#					+  * self.CommPowerState.Sleep # in mJ
			#if (minCommEnergyExpense == -1) or (CommEnergyExpense < minCommEnergyExpense):
			#	minCommEnergyExpense = minCommEnergyExpense
			#	bestCommProtocol = CommProtocol.TechnoName
		return retList
