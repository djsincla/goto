import socket
import re
import ephem
import datetime
import time

test0 = ["00003700 Tauranga [AzEl Rotor Report:Azimuth:350.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:352.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:354.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:356.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:358.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:0.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:2.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:4.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:6.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:8.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:10.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:12.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:14.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:16.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:18.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:20.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:22.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:24.87, Elevation:7.40, SatName:AO-71]"]

test1 = ["00003700 Tauranga [AzEl Rotor Report:Azimuth:160.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:164.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:168.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:172.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:174.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:176.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:178.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:180.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:182.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:184.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:188.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:192.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:196.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:200.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:204.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:208.87, Elevation:7.40, SatName:AO-71]"]

test = test0

# Open UDP Socket to receive MacDoppler 
macD = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

for x in range(0, len(test)-1):
	macD.sendto(test[x], ("127.0.0.1", 9932))
	print(test[x])
	time.sleep(4)

