class PowerState:
	def __init__(self, HWName,CPUIdle, CPUActive, Sleep):
		self.HWName = HWName
		self.CPUIdle = CPUIdle
		self.CPUActive = CPUActive
		self.Sleep = Sleep

	def __repr__(self):
		string = "\n\n\tPower Consumption:\n"
		string += "\n\t\tHardware Name = " + self.HWName
		string += "\n\t\tCPU Idle = " + str(self.CPUIdle) + " mW"
		string += "\n\t\tCPU Active = " + str(self.CPUActive) + " mW"
		string += "\n\t\tSleep = " + str(self.Sleep) + " mW"
		return string
