class Rule:
	def __init__(self, EventType, CurrentId, Incident, Action, NewId):
		self.EventType = EventType
		self.CurrentId = CurrentId
		self.Incident = Incident
		self.Action = Action
		self.NewId = NewId

	def __repr__(self):
		string = '\n\t\tRule:'
		string += '\n\t\t\tIf'
		string += '\n\t\t\t\tEvent Type = ' + str(self.EventType)
		string += '\n\t\t\t\tCurrent Id(s) = ' + ','.join(list(map(str, self.CurrentId)))
		string += '\n\t\t\t\tIncident = ' + str(self.Incident)
		string += '\n\t\t\tThen'
		string += '\n\t\t\t\tAction = ' + str(self.Action)
		string += '\n\t\t\t\tNew Id(s) = ' + ','.join(list(map(str, self.NewId)))
		return string