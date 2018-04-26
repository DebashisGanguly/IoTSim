class ProcAlgo:
	def __init__(self, Name, ProcTimePerBit, CompressionRatio, Accuracy):
		self.Name = Name
		self.ProcTimePerBit = ProcTimePerBit
		self.CompressionRatio = CompressionRatio
		self.Accuracy = Accuracy

	def __repr__(self):
		string = '\n\t\tProcessing Algorithm:'
		string += '\n\t\t\tName = ' + self.Name
		string += '\n\t\t\tProcessing Time Per Bit = ' + str(self.ProcTimePerBit) + ' ms'
		string += '\n\t\t\tCompression Ratio (data to send / processed data) = ' + str(self.CompressionRatio)
		string += '\n\t\t\tAccuracy Score = ' + str(self.Accuracy)
		return string
