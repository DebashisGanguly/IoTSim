class Battery:
	def __init__(self, InitialEnergy, BatteryLeakage, CutOffThreshold):
		self.InitialEnergy = InitialEnergy
		self.BatteryLeakage = BatteryLeakage
		self.CutOffThreshold = CutOffThreshold

	def __repr__(self):
		string =  "\n\n\tBattery:\n"
		string +=  "\n\t\tInitial Energy = " + str(self.InitialEnergy) + " mJ"
		string +=  "\n\t\tBattery Leakage = " + str(self.BatteryLeakage) + " %"
		string +=  "\n\t\tCut Off Threshold = " + str(self.CutOffThreshold) + " %"
		return string