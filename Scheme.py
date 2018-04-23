from Rule import Rule

class Scheme:
	def __init__(self, Name, Rules, DefaultWorkflowId):
		self.Name = Name
		self.Rules = Rules
		self.DefaultWorkflowId = DefaultWorkflowId
#		self.DataRate = DataRate
#		self.AcquireTime = AcquireTime
#		self.StaticPower = StaticPower
#		self.DynamicPower = DynamicPower

	def __repr__(self):
		string = '\n\t\tScheme:'
		string += '\n\t\t\tName = ' + self.Name
		string += '\n\t\t\tDefaultWorkFlowId = ' + self.DefaultWorkflowId
		for rule in self.Rules:
			string += '\n\t\t\tRule:' + '\n\t\t\t\t' + str(rule)
#		string += '\n\t\t\tSensing Period = ' + str(self.SensingPeriod) + ' ms'
#		string += '\n\t\t\tData Rate = ' + str(self.DataRate) + ' bits/second'
#		string += '\n\t\t\tAcquire Time = ' + str(self.AcquireTime) + ' ms'
#		string += '\n\t\t\tStatic Power = ' + str(self.StaticPower) + ' mW'
#		string += '\n\t\t\tDynamic Power = ' + str(self.DynamicPower) + ' mW'
		return string