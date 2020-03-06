# Goto
Satellite tracking using a goto telescope mount.

MacDoppler software outputs a udp stream every second with elevation (altitude) and azumuth of passing satellites. We listen for this stream and convert to Ioptron goto telescope mount contol commands to slew the mount to point to the satellite. This happens every second effectivly tracking the satellite across the sky.

Antennas are mounted to the iOptron telescope mount for amateur radio satellite communications.

# Three Files...

## iopt-base.py

My initial attempt. Single threaded which would action a command to the telescope when udp data was received from MacDoppler which just happens to be every second. Any pause I would make for the telescope mount would ignore udp data.

## iopt-2.py

Improved code based on three threads running simutanionsly. 
- First thread is the udp listener which updates an object when data is received.
- Second thread loops checking every 0.4 seconds for any change in object data and if so, formats and sends telescope mount commands. 
- Third thread waits on keyboard input and ends on q/Q or exception such as ctrl-c.
- Updated to work and save Altitude (elevation) and Azimuth in degrees with the conversion to telescope arcseconds commands at the time of command.

## iopt-test

Generates udp datastream to test various positions. Assisted me with debugging azimuth transitions such as 359->001.

