import threading, time, socket, click, os

TELESCOPE_IP ="10.10.100.254"
TELESCOPE_SOC = 8899
MACDOPPLER_IP ="127.0.0.1"
MACDOPPLER_SOC = 9932
TELESCOPE_INT = 0.4

class AltAz(object):
    altitude = "00000000"
    azimuth = "000000000"
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

        def Decdeg2arc(deg):
            is_positive = deg >= 0
            deg = abs(deg)
            minutes,seconds = divmod(deg*3600,60)
            degrees,minutes = divmod(minutes,60)
            degrees = degrees if is_positive else -eeedegrees 
            deg = ( (degrees * 60* 60) + (minutes * 60) + (seconds) ) * 100
            return (int(deg))

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

            self.shared.azimuth = format(int(Decdeg2arc(float(azimuth))), '09')
            self.shared.altitude = format(int(Decdeg2arc(float(altitude))), '08')
            self.shared.satName = satName
            click.echo('Computed Data for Az: ' + str(self.shared.azimuth) + ' Alt: ' + str(self.shared.altitude) + ' Name: ' + self.shared.satName+'\r')

class DoTele(threading.Thread):
    def __init__(self, shared, *args, **kwargs):
        super(DoTele,self).__init__(*args, **kwargs)
        self.shared = shared

    def run(self):

        def TelCommand(cmdD, cmd):
            teleScope.send(cmd.encode())
            r = teleScope.recv(1024)
            click.echo('Mount command:  '+cmdD+' '+cmd+'\r') 
            click.echo('Mount response: '+r+'\r') 
            return r

        click.echo('Telescope Command Thread Started...'+'\r')

        # Open TCP Socek
        teleScope = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
        teleScope.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        teleScope.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        teleScope.connect((TELESCOPE_IP, TELESCOPE_SOC))

        slewMsg = ":MS#"
        posMsg = ":GAC#"
        mountInfo = ":MountIfo#"
        stopTra = ":ST0#"

        resp = TelCommand("Mount Info", mountInfo)
        resp = TelCommand("Stop Tracking", stopTra)

        resp = TelCommand("Current Position", posMsg)
        self.shared.altitude = resp[1:9]
        self.shared.azimuth = resp[9:18]

        lastAltitude = self.shared.altitude
        lastAzimuth =  self.shared.azimuth

        #:Sas32400000# Elevation
        #:Sz064800000# Azimuth

        while True:

            if self.shared.altitude != lastAltitude or self.shared.azimuth != lastAzimuth:

                elMsg = ":Sa+" + self.shared.altitude + "#" 
                azMsg = ":Sz" + self.shared.azimuth + "#"
                resp = TelCommand("Set Azimuth", azMsg)
                resp = TelCommand("Set Elevation", elMsg)
                resp = TelCommand("Slew", slewMsg)
                lastAltitude = self.shared.altitude
                lastAzimuth =  self.shared.azimuth

                resp = TelCommand("Current Position", posMsg)
                testEl = resp[1:9]
                testAz = resp[9:18]

                absTestEl = abs(int(testEl) - int(self.shared.altitude))
                absTestAz = abs(int(testAz) - int(self.shared.azimuth))

                if absTestAz > (180*3600*100):
                    absTestAz = (360*3600*100) - absTestAz 
                if absTestAz > 5000000 or absTestEl > 5000000:
                    click.echo('Difference in El: '+str(absTestEl)+' Difference in Az: '+str(absTestAz)+'\r')
                    secsEl = absTestEl  / 7500000
                    secsAz = absTestAz  / 6000000
                    secsEl = int(secsEl)
                    secsAz = int(secsAz)
                    sleepSecs = [4, secsEl, secsAz]
                    click.echo('Pausing '+str(max(sleepSecs))+' seconds to Slew....'+'\r')
                    time.sleep(int(max(sleepSecs)))
                    click.echo('Now continuing.'+'\r')

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

