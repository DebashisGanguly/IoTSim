from Rule import Rule

class Scheme:
	def __init__(self, Name, Rules, DefaultWorkflowId):
		self.Name = Name
		self.Rules = Rules
		self.DefaultWorkflowId = DefaultWorkflowId

	def __repr__(self):
		string = '\n\t\tScheme:'
		string += '\n\t\t\tName = ' + self.Name
		string += '\n\t\t\tDefaultWorkFlowId = ' + self.DefaultWorkflowId
		for rule in self.Rules:
			string += '\n\t\t\tRule:' + '\n\t\t\t\t' + str(rule)
		return string
