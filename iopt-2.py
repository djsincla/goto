import threading, time, socket, click, os

# 2 -> 24 Rewritten to work with altitude and azimuth in degrees. Conversion to telescope will happen at command executioon time.
# This will make future work 

TELESCOPE_IP ="10.10.100.254"
TELESCOPE_SOC = 8899
MACDOPPLER_IP ="127.0.0.1"
MACDOPPLER_SOC = 9932
TELESCOPE_INT = 0.4

class AltAz(object):
    altitude = 30.00
    azimuth = 240.00
    satName = "None"

class DoMacD(threading.Thread):
    def __init__(self, shared, *args, **kwargs):
        super(DoMacD,self).__init__(*args, **kwargs)
        self.shared = shared

    def run(self):

        def ParseDopData(macDopData):
            # print("received message: %s"%data)
            # 00002008 Tauranga [AzEl Rotor Report:Azimuth:90.00, Elevation:20.00, SatName:AO-92]
            aziParsed = macDopData.split(",")[0]
            aziParsed = aziParsed.split(":")[2]
            altParsed = macDopData.split(",")[1]
            altParsed = altParsed.split(":")[1]
            satNameParsed = macDopData.split(",")[2]
            satNameParsed = satNameParsed.split(']')[0]
            satNameParsed = satNameParsed.split(':')[1]
            return aziParsed, altParsed, satNameParsed

        click.echo('MacDopper Monitor Thread Started...'+'\r')

        # Open UDP Socket to receive MacDoppler 
        macD = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # UDP
        macD.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        macD.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        macD.bind(("", MACDOPPLER_SOC))

        while True:
            data, addr = macD.recvfrom(1024)

            click.clear()
            click.echo('Data received: '+str(data)+'\r')
            azimuth, altitude, satName = ParseDopData(str(data))
            click.echo('Parsed Data for Az: ' + str(azimuth) + ' Alt: ' + str(altitude) + ' Name: '+ satName+'\r')

            self.shared.azimuth = azimuth
            self.shared.altitude = altitude
            self.shared.satName = satName

class DoTele(threading.Thread):
    def __init__(self, shared, *args, **kwargs):
        super(DoTele,self).__init__(*args, **kwargs)
        self.shared = shared

    def run(self):

        def DecDeg2arc(deg):
            is_positive = deg >= 0
            deg = abs(deg)
            minutes,seconds = divmod(deg*3600,60)
            degrees,minutes = divmod(minutes,60)
            degrees = degrees if is_positive else -eeedegrees 
            arc = int(( (degrees * 60* 60) + (minutes * 60) + (seconds) ) * 100)
            return arc

        def Arc2DecDeg(arc):
            arc = abs(int(arc))
            degrees, seconds = divmod(arc, (3600*100))
            subSecs1, remain = divmod(seconds, (360*100))
            subSecs2, remain = divmod(remain, (360*10))
            deg = float(str(str(degrees)+'.'+str(subSecs1)+str(subSecs2)))
            return deg

        def TelCommand(cmdD, cmd):
            click.echo('Mount command:  '+cmdD+' '+cmd+'\r')
            teleScope.send(cmd.encode())
            try:
                r = teleScope.recv(1024)            
                click.echo('Mount response: '+r+'\r') 
            except:
                click.echo('Timeout waiting for response'+'\r')
                r = 'Timeout'
            return r

        click.echo('Telescope Command Thread Started...'+'\r')

        # Open TCP Socek
        teleScope = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
        #teleScope = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # UDP
        teleScope.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        teleScope.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        teleScope.connect((TELESCOPE_IP, TELESCOPE_SOC))
        teleScope.settimeout(20)

        slewMsg = ":MS#"
        posMsg = ":GAC#"
        mountInfo = ":MountInfo#"
        stopTra = ":ST0#"

        resp = TelCommand("Mount Info", mountInfo)
        resp = TelCommand("Stop Tracking", stopTra)
        resp = TelCommand("Current Position", posMsg)
        self.shared.altitude = Arc2DecDeg(resp[1:9])
        self.shared.azimuth = Arc2DecDeg(resp[9:18])
        click.echo("Current Position: Al "+str(self.shared.altitude)+ ' Az '+str(self.shared.azimuth)+'\r')
        lastAltitude = self.shared.altitude
        lastAzimuth =  self.shared.azimuth

        #:Sas32400000# Elevation
        #:Sz064800000# Azimuth

        while True:

            if self.shared.altitude != lastAltitude or self.shared.azimuth != lastAzimuth:

                resp = TelCommand("Current Position", posMsg)
                if len(resp) == 19:

                    testAl = Arc2DecDeg(resp[1:9])
                    testAz = Arc2DecDeg(resp[9:18])
                    click.echo('Current Position: Az '+str(testAz)+' Al '+str(testAl)+'\r')
                    click.echo('Desired Position: Az '+self.shared.azimuth+' Al '+self.shared.altitude+'\r')
                    absTestAl = abs((90.0 - float(testAl)) - (90.0 - float(self.shared.altitude)))
                    absTestAz = abs((360.0 - float(testAz)) - (360.0 - float(self.shared.azimuth)))

                    elMsg = ":Sa+" + format(int(DecDeg2arc(float(self.shared.altitude))), '08') + "#" 
                    azMsg = ":Sz" + format(int(DecDeg2arc(float(self.shared.azimuth))), '09') + "#"
                    resp = TelCommand("Set Azimuth", azMsg)
                    resp = TelCommand("Set Elevation", elMsg)
                    resp = TelCommand("Slew", slewMsg)
                    lastAltitude = self.shared.altitude
                    lastAzimuth =  self.shared.azimuth

                    if absTestAz > 30.0 or absTestAl > 30.0:
                        click.echo('Difference in Az '+str(absTestAz)+' Difference in Al: '+str(absTestAl)+'\r')
                        secsAl = absTestAl  / 12.0
                        secsAz = absTestAz  / 12.0
                        secsAl = int(secsAl)
                        secsAz = int(secsAz)
                        sleepSecs = [4, secsAl, secsAz]
                        click.echo('Pausing '+str(max(sleepSecs))+' seconds to Slew...'+'\r')
                        time.sleep(int(max(sleepSecs)))
                        click.echo('Now continuing...'+'\r')

            time.sleep(TELESCOPE_INT)

class KeyClick(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(KeyClick,self).__init__(*args, **kwargs)

    def run(self):
        click.echo('Keyboard Monitoring Thread Started...'+'\r')
        while True:
            try:
                c = click.getchar()
                click.echo()
                if c == 'Q' or c == 'q':
                    click.echo('Quitting...'+'\r')
                    os._exit(1)
            except:
                click.echo('Quitting...'+'\r')
                os._exit(1)

def main():
    ## Mainline below...

    # Clear the screen.
    click.clear()

    threads = [ DoMacD(shared=AltAz, name='a'), 
                DoTele(shared=AltAz, name='b'),
                KeyClick(name='c')
                ]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

if __name__ == '__main__':
    main()

