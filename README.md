# goto
Satellite tracking using a goto telescope mount.

MacDoppler software outputs a udp stream every second with elevation (altitude) and azumuth of passing satellites. We listen for this stream and convert to Ioptron goto telescope mount contol commands to slew the mount to point to the satellite. This happens every second effectivly tracking the satellite across the sky.

Antennas are mounted to the Ioptron telescope mount for amateur radio satellite communications.
