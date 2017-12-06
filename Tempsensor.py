# usr/bin/python
# Cody Purcell
#https://www.sunfounder.com/learn/sensor-kit-v2-0-for-b/lesson-26-ds18b20-temperature-sensor-sensor-kit-v2-0-for-b.html
import os
import socket
import time
import Adafruit_CharLCD as LCD

logfile = open("LCDDisplay.log",'a')
lcd = LCD.Adafruit_CharLCDPlate()

SERVERIP = "10.0.0.22"
n = 0

ds18b20 = ''

def setup():
	global ds18b20
	for i in os.listdir('/sys/bus/w1/devices'):
		if i != 'w1_bus_master1':
			ds18b20 = i

def read():
#	global ds18b20
	location = '/sys/bus/w1/devices/' + ds18b20 + '/w1_slave'
	tfile = open(location)
	text = tfile.read()
	tfile.close()
	secondline = text.split("\n")[1]
	temperaturedata = secondline.split(" ")[9]
	temperature = float(temperaturedata[2:])
	temperature = temperature  / 1000
	Celsius = float(temperature)
	Fahrenheit = 9.0/5.0 * Celsius + 32
	return temperature

	
def loop():
        global n
        while True:
                if read() != None:
                        C = read()
                        F = 9.0/5.0 * C + 32
                        print "Current Temperature : %0.6f F" % F
                        output_string = "Temperature is: \n %.1f F" % F
                        time.sleep(5)
                        lcd.message(output_string)
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.connect((SERVERIP,8881))
                        print "%d : Connected to server" % n,
                        data = "'CodyPurcell', %d , %0.6f F" % (n, F)
                        sock.sendall(data)
                        print " Sent :", data
                        sock.close( )
                        n += 1
                        time.sleep(5)
                        lcd.clear()

def destroy():
	pass

if __name__ == '__main__':
	try:
		setup()
		loop()
	except KeyboardInterrupt:
		destroy()
