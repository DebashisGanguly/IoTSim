class CommPowerState:
	def __init__(self, HWName, Rx, Tx, CPUIdle, CPUActive, Sleep):
		self.HWName = HWName
		self.Rx = Rx
		self.Tx = Tx
		self.CPUIdle = CPUIdle
		self.CPUActive = CPUActive
		self.Sleep = Sleep

	def __repr__(self):
		string = "\n\n\tPower Consumption:\n"
		string += "\n\t\tHardware Name = " + self.HWName
		string += "\n\t\tRx = " + str(self.Rx) + " mW"
		string += "\n\t\tTx = " + str(self.Tx) + " mW"
		string += "\n\t\tCPU Idle = " + str(self.CPUIdle) + " mW"
		string += "\n\t\tCPU Active = " + str(self.CPUActive) + " mW"
		string += "\n\t\tSleep = " + str(self.Sleep) + " mW"
		return string