# IoTSim

#Configuration Parameters
	
	Units:
		Application Period: ms
		Application Data Size: kB
		Granularity: s

	#Battery Parameters

		Units:	
			
			BatteryLeakage: percentage
			CutOffThreshold: percentage

		Details of Specific Parameter:
			
			Initial Energy = 2 * AAA = 2 * 1250 (mAh) * 1.5 (V) = 3,750 Wh = 13.5 kJ = 13500000 mJ

	#Network Protocol Hardware Parameters

		Units:
			
			Maximum Packet Size: bytes
			PHY Rate: Mbps
			PHY Overhead: us
			MAC Overhead: bits
			IPv6 Overhead: bits
			Synchro Period: ms
			Clock Accuracy: ppm (ppmRX - ppmTX)
			Packet Delivery Ratio: percentage
			Power: mW

		Protocol Name: BLE5.0, 1Mbps
			
			Details of Specific Parameter:
				
				Hardware Name: nRF51822

				LLDataHeader = 32 bits
				MAC Overhead = 16 +  LLDataHeader = 48 bits (No MIC)
				
				Voltage= 3.0 V
				CPU Idle Power = 0.275 * 16 * Voltage = 13.2 [0.275 mA/MHz (read from flash) * CPU Freq (16MHz)]
				Rx Power = CPU Idle Power + 9.7 * Voltage = 42.3 
				Tx Power = CPU Idle Power + 8 * Voltage = 37.2
				Sleep Mode Power = 2.6 * 10^(-3) * Voltage = 0.0078

		Protocol Name: 802.11ah - MCS9, 16MHz
			
			Details of Specific Parameter:

				Hardware Name: 200Rx
				
				Synchro Period = pow(10,4) * (pow(2,14)-1) * pow(10,3) = 163830000000 ms 
				
				Voltage= 3.0 V
				CPU Idle Power = 10 * Voltage = 30 V
				Rx Power = CPU Idle Power + 200 = 230 V 
				Tx Power = 400 V
				Sleep Mode Power = 2.5 * 10^(-3) * Voltage = 0.0075 V
