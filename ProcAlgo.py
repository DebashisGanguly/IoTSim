class ProcAlgo:
	def __init__(self, Name, ProcTimePerBit, CompressionRatio):
		self.Name = Name
		self.ProcTimePerBit = ProcTimePerBit
		self.CompressionRatio = CompressionRatio

	def __repr__(self):
		string = '\n\t\tProcessing Algorithm:'
		string += '\n\t\t\tName = ' + self.Name
		string += '\n\t\t\tProcessing Time Per Bit = ' + str(self.ProcTimePerBit) + ' ms'
		string += '\n\t\t\tCompression Ratio (data to send / processed data) = ' + str(self.CompressionRatio)
		return string