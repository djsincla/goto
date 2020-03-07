import threading, time, socket, click, os
from socket import SHUT_RDWR

# February 2020
# Dwayne Sinclair NA6US

# Python script to drive a goto telecope via slew commands. 
# This script is optimized to work with a ioptron AZ Mount Pro AltAz mount via TCP/IP.

# Three threads in this program run insdependent of each other.
#   DoMacD Thread monitors UDP stream from MacDoppler and updates shared objects with elevation (altitude) and aximuth.
#   Frequency from MacDoppler is 1 second but it could be any frequency.
#
#   DoTele thread monitors changes to azimuth and altitude in the shared object will command the telescope mount to slew to the new
#   if a change is found.
#
#   KeyClick thread is monitoring for Q/q command and Control-C

# FYI's
# - The AZ Mount Pro appears not to pass through 360 degrees. Best to set it up pointing south so mount should not
#   stretch cables more than 180 degrees in either direction.
# - The TCP/IP implementation is based on the RS232 implementation and needs to be "blocking" given if commands are send async, the 1's and 0's 
#   command responses have to be associated with the commands than sent them.
# - There is provision for long slews where the program will wait for a period of the for the slew to complete. This is because sending
#   a slew command when the mount is already slewing will cause the mount to stop and restart.

# Bugs
# - There appears to be a 5 second lag responding to commands now and then on TCP/IP. This does not affect operation and I have opened a support 
#   ticket with iOptron.
# - I need to add logic to close and reopen the TCP/IP session to the mount after inactivity of say 10 minutes. Long pauses between satellites
#   and the session is dead requiring a program restart.

# Latest changes:
# 3/5/20 DJS - Updated to save altitude and azimuth in degrees. Arcunit conversion will occur when sending command to telescope mount.
#              This will make swapping commands for a different scope easier. 

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
            click.echo(str(data)+'\r')
            azimuth, altitude, satName = ParseDopData(str(data))
            click.echo('Parsed Data - Azi: ' + str(azimuth) + ' Alt: ' + str(altitude) + ' Name: '+ satName+'\r')

            self.shared.azimuth = azimuth
            self.shared.altitude = altitude
            self.shared.satName = satName

class DoTele(threading.Thread):

    def __init__(self, shared, *args, **kwargs):
        super(DoTele,self).__init__(*args, **kwargs)
        self.shared = shared

    def run(self):

        def MountOpen():
            mountOpenObj = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
            #teleScope = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # UDP
            mountOpenObj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            mountOpenObj.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            mountOpenObj.settimeout(20)
            try:
                click.echo('Opening Telescope Mount TCP Session.'+'\r')
                mountOpenObj.connect((TELESCOPE_IP, TELESCOPE_SOC))
            except Exception:
                click.echo('Error Opening Telescope Mount. Quitting.'+'\r')
                os._exit(1)
            return mountOpenObj

        def MountClose(mountCloseObj):
            try:
                click.echo('Closing Telescope Mount TCP Session.'+'\r')
                mountCloseObj.shutdown(SHUT_RDWR)
                mountCloseObj.close()
            except Exception:
                click.echo('Error Closing Telescope Mount. Quitting.'+'\r')
                os._exit(1)
            return

        def MountCommand(cmdD, cmd, TelCommandObj):
            click.echo('Mount command:  '+cmdD+' '+cmd+'\r')
            TelCommandObj.send(cmd.encode())
            try:
                r = TelCommandObj.recv(1024)            
                click.echo('Mount response: '+r+'\r') 
            except:
                click.echo('Timeout waiting for response'+'\r')
                r = 'Timeout'
            return r

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


        click.echo('Telescope Command Thread Started...'+'\r')

        slewMsg = ":MS#"
        posMsg = ":GAC#"
        mountInfo = ":MountInfo#"
        stopTra = ":ST0#"

        teleScope = MountOpen()

        resp = MountCommand("Mount Info", mountInfo, teleScope)
        resp = MountCommand("Stop Tracking", stopTra, teleScope)
        resp = MountCommand("Current Position", posMsg, teleScope)
        # Its possible we receive a positive reponse to a previous command concatinated with the 
        # position report. We parse from the end of the string.
        lenP = len(resp)
        self.shared.altitude = Arc2DecDeg(resp[lenP-18:lenP-10])
        self.shared.azimuth = Arc2DecDeg(resp[lenP-10:lenP-1])
        click.echo("Current Position: Azi: "+str(self.shared.azimuth)+ ' Alt: '+str(self.shared.altitude)+'\r')
        lastAltitude = self.shared.altitude
        lastAzimuth =  self.shared.azimuth

        mountConnect = True
        idleTime = 0.0
        numLoops = 0
        maxLoops = 25

        while True:

            if self.shared.altitude != lastAltitude or self.shared.azimuth != lastAzimuth:

                idleTime = 0.0
                numLoops = numLoops + 1

                # If Telescope Mount TCP Session is not open, we open it.
                if mountConnect != True:
                    teleScope = MountOpen()
                    mountConnect = True

                resp = MountCommand("Current Position", posMsg, teleScope)
                if len(resp) >= 19:
                    # Its possible we receive a positive reponse to a previous command concatinated with the 
                    # position report. We parse from the end of the string.
                    lenP = len(resp)
                    testAl = Arc2DecDeg(resp[lenP-18:lenP-10])
                    testAz = Arc2DecDeg(resp[lenP-10:lenP-1])
                    click.echo('Current Position: Azi: '+str(testAz)+' Alt: '+str(testAl)+'\r')
                    click.echo('Desired Position: Azi: '+self.shared.azimuth+' Alt: '+self.shared.altitude+'\r')
                    absTestAl = abs((90.0 - float(testAl)) - (90.0 - float(self.shared.altitude)))
                    absTestAz = abs((360.0 - float(testAz)) - (360.0 - float(self.shared.azimuth)))

                    elMsg = ":Sa+" + format(int(DecDeg2arc(float(self.shared.altitude))), '08') + "#" 
                    azMsg = ":Sz" + format(int(DecDeg2arc(float(self.shared.azimuth))), '09') + "#"
                    resp = MountCommand("Set Azimuth", azMsg, teleScope)
                    resp = MountCommand("Set Elevation", elMsg, teleScope)
                    resp = MountCommand("Slew", slewMsg, teleScope)
                    lastAltitude = self.shared.altitude
                    lastAzimuth =  self.shared.azimuth

                    # Checking to see if its a big slew and if so, we wait for some seconds for the slew to complete
                    if absTestAz > 20.0 or absTestAl > 20.0:
                        click.echo('Difference in Azi: '+str(absTestAz)+' Difference in Alt: '+str(absTestAl)+'\r')
                        # These divisions should generate a good time to wait.
                        secsAl = absTestAl  / 11.0
                        secsAz = absTestAz  / 11.0
                        secsAl = int(secsAl)
                        secsAz = int(secsAz)
                        # three possible values to sleep including the default of 4 seconds.
                        # We will sleep the highest value.
                        sleepSecs = [4, secsAl, secsAz]
                        click.echo('Pausing '+str(max(sleepSecs))+' seconds to Slew...'+'\r')
                        time.sleep(int(max(sleepSecs)))
                        click.echo('Now continuing...'+'\r')

            time.sleep(TELESCOPE_INT)
            idleTime = idleTime + TELESCOPE_INT
            # No need to maintain the Telescope Mount TCP Session. Close it after 10 seconds on inactivity.
            if ( idleTime > 10.0 or numLoops > maxLoops ) and mountConnect != False:
                MountClose(teleScope)
                mountConnect = False
                numLoops = 0


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

