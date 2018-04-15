class ProcAlgo:
	def __init__(self, Name, ProcTimePerBit):
		self.Name = Name
		self.ProcTimePerBit = ProcTimePerBit

	def __repr__(self):
		string = '\n\t\tProcessing Algorithm:'
		string += '\n\t\t\tName = ' + self.Name
		string += '\n\t\t\tProcessing Time Per Bit = ' + str(self.ProcTimePerBit) + ' ms'
		return string