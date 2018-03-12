class CommPowerState:
	def __init__(self, HWName, Rx, Tx, CPUIdle, Sleep):
		self.HWName = HWName
		self.Rx = Rx
		self.Tx = Tx
		self.CPUIdle = CPUIdle
		self.Sleep = Sleep

	def __repr__(self):
		string = "\n\n\t\t\tPower Consumption:\n"
		string += "\n\t\t\t\tHardware Name = " + self.HWName
		string += "\n\t\t\t\tRx = " + str(self.Rx) + " mW"
		string += "\n\t\t\t\tTx = " + str(self.Tx) + " mW"
		string += "\n\t\t\t\tCPU Idle = " + str(self.CPUIdle) + " mW"
		string += "\n\t\t\t\tSleep = " + str(self.Sleep) + " mW"
		return string