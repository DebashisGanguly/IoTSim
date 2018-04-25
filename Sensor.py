class Sensor:
	def __init__(self, Name, SensingPeriod, DataRate, AcquireTime, StaticPower, DynamicPower, Criticality):
		self.Name = Name
		self.SensingPeriod = SensingPeriod
		self.DataRate = DataRate
		self.AcquireTime = AcquireTime
		self.StaticPower = StaticPower
		self.DynamicPower = DynamicPower
		self.Criticality = Criticality


	def __repr__(self):
		string = '\n\t\tSensor:'
		string += '\n\t\t\tName = ' + self.Name
		string += '\n\t\t\tSensing Period = ' + str(self.SensingPeriod) + ' ms'
		string += '\n\t\t\tData Rate = ' + str(self.DataRate) + ' bits/second'
		string += '\n\t\t\tAcquire Time = ' + str(self.AcquireTime) + ' ms'
		string += '\n\t\t\tStatic Power = ' + str(self.StaticPower) + ' mW'
		string += '\n\t\t\tDynamic Power = ' + str(self.DynamicPower) + ' mW'
		string += '\n\t\t\tCriticality score = ' + str(self.Criticality)
		return string