import socket
import re
import ephem
from PyAstronomy import pyasl
import datetime
import time

# If Telescope Mount requires RA/DEC we need lat. long, and altitude to calculate
# These are your viewing location.
lat = 33.8266 #deg
lon = -118.387 #deg
alt = 10.0 #m

def Decdeg2arc(deg):
	is_positive = deg >= 0
	deg = abs(deg)
	minutes,seconds = divmod(deg*3600,60)
	degrees,minutes = divmod(minutes,60)
	degrees = degrees if is_positive else -degrees 
	deg = ( (degrees * 60* 60) + (minutes * 60) + (seconds) ) * 100
	return (int(deg))

def ParseDopData(macDopData):
	# print("received message: %s"%data)
	# 00002008 Tauranga [AzEl Rotor Report:Azimuth:90.00, Elevation:20.00, SatName:AO-92]
	aziParsed = macDopData.split(",")[0]
	aziParsed = aziParsed.split(":")[2]
	eleParsed = macDopData.split(",")[1]
	eleParsed = eleParsed.split(":")[1]
	satNameParsed = macDopData.split(",")[2]
	satNameParsed = satNameParsed.split(']')[0]
	satNameParsed = satNameParsed.split(':')[1]
	return aziParsed, eleParsed, satNameParsed

def ConvertAzEl2RaDec(az,el):

	ut = pyasl.get_juldate() #julian date
	# Which Julian Date does Ephem start its own count at?
	J0 = ephem.julian_date(0)
	observer = ephem.Observer()
	observer.lon = str(lon)  # str() forces deg -> rad conversion
	observer.lat = str(lat)  # deg -> rad
	observer.elevation = alt
	observer.date = ut - J0
	resultRaDec = observer.radec_of(az, el)

	return resultRaDec

def TelCommand(cmdD, cmd):
	teleScope.send(cmd.encode())
	r = teleScope.recv(1024)
	print("Mount command:  "+cmdD+" "+cmd) 
	print("Mount response: "+r) 

	return r

# Open UDP Socket to receive MacDoppler 
macD = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # UDP
macD.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
macD.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
macD.bind(("", 9932))

# Open TCP Socek
teleScope = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
teleScope.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
teleScope.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
teleScope.connect(("10.10.100.254", 8899))

slewMsg = ":MS#"
posMsg = ":GAC#"
mountInfo = ":MountIfo#"
stopTra = ":ST0#"

resp = TelCommand("Mount Info", mountInfo)
resp = TelCommand("Stop Tracking", stopTra)

while True:
	data, addr = macD.recvfrom(1024)

	print("Data received: "+data)
	azimuth, elevation, satName = ParseDopData(data)

	azimuthDms = format(int(Decdeg2arc(float(azimuth))), "09")
	elevationDms = format(int(Decdeg2arc(float(elevation))), "08")
	print("Parsed Data is Az: " + str(azimuthDms) + " Elev: " + str(elevationDms) + " Name: " + satName)

	raDec = ConvertAzEl2RaDec(azimuth,elevation)
	ra = raDec[0]
	de = raDec[1]
	print("Calculated ra and dec: " + str(ra) + " " + str(de) )

	#:Sas32400000# Elevation
	#:Sz064800000# Azimuth

	elMsg = ":Sa+" + elevationDms + "#" 
	azMsg = ":Sz" + azimuthDms + "#"

	resp = TelCommand("Stop Tracking", stopTra)
	resp = TelCommand("Set Azimuth", azMsg)
	resp = TelCommand("Set Elevation", elMsg)
	resp = TelCommand("Slew", slewMsg)

	resp = TelCommand("Current Position", posMsg)
	if resp != '' :
		testEl = resp[1:9]
		testAz = resp[9:18]
		print("Test Az 1: "+str(testAz))
		print("Test El 1: "+str(testEl))
		absTestEl = abs(int(testEl) - int(elevationDms))
		absTestAz = abs(int(testAz) - int(azimuthDms))
		print("Test Az 2: "+str(absTestAz))
		print("Test El 2: "+str(absTestEl))
		if absTestAz > (180*3600*100):
			absTestAz = (360*3600*100) - absTestAz 
		if absTestAz > 5000000 or absTestEl > 5000000:
			print("Difference in El: "+str(absTestEl))
			print("Difference in Az: "+str(absTestAz))
			secsEl = absTestEl  / 7500000
			secsAz = absTestAz  / 10000000
			secsEl = int(secsEl)
			secsAz = int(secsAz)
			sleepSecs = [4, secsEl, secsAz]
			print("Pausing "+str(max(sleepSecs))+" seconds to Slew....")
#			if abs(int(testEl) - int(elevationDms))
			time.sleep(int(max(sleepSecs)))
			print("Now continuing.")
	else:
		print("No position report returned.")









