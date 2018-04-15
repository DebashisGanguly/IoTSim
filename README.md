IoTSim

Configuration Parameters

	Power Consumption State

		Hardware Name: nRF51822

			Voltage= 3.0 V
			CPU Idle Power = 0.275 * 16 * Voltage = 13.2 [0.275 mA/MHz (read from flash) * CPU Freq (16MHz)]
			Rx Power = CPU Idle Power + 9.7 * Voltage = 42.3 
			Tx Power = CPU Idle Power + 8 * Voltage = 37.2
			Sleep Mode Power = 2.6 * 10^(-3) * Voltage = 0.0078

		Hardware Name: 200Rx

			Voltage= 3.0 V
			CPU Idle Power = 10 * Voltage = 30 V
			Rx Power = CPU Idle Power + 200 = 230 V 
			Tx Power = 400 V
			Sleep Mode Power = 2.5 * 10^(-3) * Voltage = 0.0075 V

	Sensors Paramters
	
        Units:
	
	        Sensing Period: ms
	        Data Rate: bits/second
	        Data Acquisition time: ms
	        Static Power: mW
	        Dynamic Power: mW
			Default Sensing Period: ms
				
	Processing Algorithm Parameters
	
		Units:
		
			Time to process aquired sensor data: ms/bit
			
	Network Protocol Hardware Parameters

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
				
				LLDataHeader = 32 bits
				MAC Overhead = 16 +  LLDataHeader = 48 bits (No MIC)
				TIFS = 150 us

		Protocol Name: 802.11ah - MCS9, 16MHz
			
			Details of Specific Parameter:
				
				Synchro Period = pow(10,4) * (pow(2,14)-1) * pow(10,3) = 163830000000 ms 
				
				SIFS = 160.0 us
				DIFS= 264 us 
				backoff= 0 us
				
				fc = 2 bytes
				duration = 2 bytes
				senderAddress = 6 bytes
				FCS = 4 bytes
				timestamp = 4 bytes
				BI = 2 bytes
				capability = 2 bytes
				IEheader = 2 bytes # Id, length
				SSID = 0 byte # 0 (broadcast) to 32
				Rates = 1 byte # 1 to 8 (each octet describe a single supported rate in unit of 500kbps)	   
				DSParameterSet = 1 byte #current channel
				TIM = 4 bytes # DTIM Count (1), DTIM Period (1), Bitmap ctrl (1), Partial virtual bitmap (1-251)

