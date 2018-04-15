class Workflow:
	def __init__(self, SensorId, ProcAlgoId, ProtocolId):
		self.SensorId = SensorId
		self.ProcAlgoId = ProcAlgoId
		self.ProtocolId = ProtocolId

	def __repr__(self):
		string = '\n\t\tWorkflow:'
		
		string += '\n\t\t\tSensor Id = ' 
		
		if self.SensorId == 0:
			string += 'None'
		elif self.SensorId == -1:
			string += 'Any'
		else:
			string += str(self.SensorId)
		
		string += '\n\t\t\tProcesssing Algorithm Id = '
		
		if self.ProcAlgoId == 0:
			string += 'None'
		elif self.ProcAlgoId == -1:
			string += 'Any'
		else:
			string += str(self.ProcAlgoId)
		
		string += '\n\t\t\tNetworking Protocol Id = ' 

		if self.ProtocolId == 0:
			string += 'None'
		elif self.ProtocolId == -1:
			string += 'Any'
		else:
			string += str(self.ProtocolId)
		
		return string