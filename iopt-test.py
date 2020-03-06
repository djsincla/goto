import socket
import re
import ephem
import datetime
import time
import threading
import click
import os


class DoTest(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(DoTest,self).__init__(*args, **kwargs)

    def run(self):

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
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:176.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:180.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:184.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:188.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:192.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:196.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:200.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:204.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:208.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:212.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:216.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:220.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:224.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:228.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:232.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:236.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:240.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:244.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:248.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:252.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:256.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:260.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:264.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:268.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:272.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:276.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:280.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:284.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:288.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:292.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:296.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:300.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:304.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:308.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:312.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:316.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:320.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:324.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:328.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:332.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:336.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:340.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:344.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:348.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:352.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:356.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:0.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:4.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:8.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:12.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:16.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:20.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:24.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:28.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:32.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:36.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:40.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:44.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:48.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:52.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:56.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:60.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:64.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:68.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:72.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:76.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:80.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:84.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:88.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:92.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:96.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:100.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:104.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:108.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:112.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:116.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:120.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:124.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:128.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:132.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:136.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:140.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:144.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:148.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:152.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:156.87, Elevation:7.40, SatName:AO-71]"]


		test3 = ["00003700 Tauranga [AzEl Rotor Report:Azimuth:240.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:300.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:0.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:60.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:120.87, Elevation:7.40, SatName:AO-71]",
		"00003700 Tauranga [AzEl Rotor Report:Azimuth:180.87, Elevation:7.40, SatName:AO-71]"]

		test = test2

		click.echo('Test Position Reports Thread Started...'+'\r')

		# Open UDP Socket to receive MacDoppler 
		macD = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

		#for x in range(0, len(test)):
		for x in range(len(test)-1, -1, -1):

			macD.sendto(test[x], ("127.0.0.1", 9932))
			click.echo(test[x]+'\r')
			time.sleep(2)


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

    threads = [ DoTest(name='a'), 
                KeyClick(name='b')
                ]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

if __name__ == '__main__':
    main()

