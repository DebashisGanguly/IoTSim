class Battery:
	def __init__(self, InitialEnergy, BatteryLeakage, CutOffThreshold, ApplicationPeriod):
		self.InitialEnergy = InitialEnergy
		self.BatteryLeakage = BatteryLeakage
		self.CutOffThreshold = CutOffThreshold
		self.ApplicationPeriod = ApplicationPeriod
		self.RemainingEnergy = self.InitialEnergy
		self.CutOffEnergy = self.InitialEnergy * self.CutOffThreshold / 100
		self.LeakageEnergy = self.InitialEnergy * (self.BatteryLeakage / 100) * (self.ApplicationPeriod / (365 * 24 * 3600 * 1000))

	def __repr__(self):
		string =  "\n\n\tBattery:\n"
		string +=  "\n\t\tInitial Energy = " + str(self.InitialEnergy) + " mJ"
		string +=  "\n\t\tBattery Leakage = " + str(self.BatteryLeakage) + " %"
		string +=  "\n\t\tCut Off Threshold = " + str(self.CutOffThreshold) + " %"
		return string

	def canSupportDevice(self):
		return (self.RemainingEnergy >= self.CutOffEnergy)

	def updateBatteryState(self, consumedEnergy):
		self.RemainingEnergy = self.RemainingEnergy - self.LeakageEnergy - consumedEnergy
		self.LeakageEnergy = self.RemainingEnergy * (self.BatteryLeakage / 100) * (self.ApplicationPeriod / (365 * 24 * 3600 * 1000))
