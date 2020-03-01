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

test2 = ["00003700 Tauranga [AzEl Rotor Report:Azimuth:160.87, Elevation:7.40, SatName:AO-71]",
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
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:208.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:212.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:214.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:218.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:222.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:226.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:230.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:234.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:238.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:242.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:246.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:250.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:254.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:258.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:262.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:266.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:270.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:274.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:278.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:282.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:286.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:290.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:294.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:298.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:302.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:306.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:310.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:314.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:318.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:322.87, Elevation:7.40, SatName:AO-71]"]

test3 = ["00003700 Tauranga [AzEl Rotor Report:Azimuth:240.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:300.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:0.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:60.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:120.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:180.87, Elevation:7.40, SatName:AO-71]"]

test = test3

# Open UDP Socket to receive MacDoppler 
macD = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

for x in range(0, len(test)):
	macD.sendto(test[x], ("127.0.0.1", 9932))
	print(test[x])
	time.sleep(7)

