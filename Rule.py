class Rule:
	def __init__(self, Name, SensingPeriod, DataRate, AcquireTime, StaticPower, DynamicPower):
		self.Name = Name
		self.SensingPeriod = SensingPeriod
		self.DataRate = DataRate
		self.AcquireTime = AcquireTime
		self.StaticPower = StaticPower
		self.DynamicPower = DynamicPower

	def __repr__(self):
		string = '\nSensor:'
		string += '\n\tName = ' + self.Name
		string += '\n\tSensing Period = ' + str(self.SensingPeriod) + ' ms'
		string += '\n\tData Rate = ' + str(self.DataRate) + ' bits/second'
		string += '\n\tAcquire Time = ' + str(self.AcquireTime) + ' ms'
		string += '\n\tStatic Power = ' + str(self.StaticPower) + ' mW'
		string += '\n\tDynamic Power = ' + str(self.DynamicPower) + ' mW'
		return string