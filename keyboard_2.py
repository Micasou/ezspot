import RPi.GPIO as GPIO
import requests
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

MATRIX = [ [1,2,3,'A'],
           [4,5,6,'B'],
           [7,8,9,'C'],
           ['*',0,'#','D'] ]

ID = ""
counter = 0

ROW = [31,33,35,37]
COL = [32,36,38,40]

for j in range(4):
    GPIO.setup(COL[j], GPIO.OUT)
    GPIO.output(COL[j], 1)

for i in range(4) :
    GPIO.setup(ROW[i], GPIO.IN, pull_up_down = GPIO.PUD_UP)

try:
    while (True):
        for j in range(4):
            GPIO.output(COL[j], 0)

            for i in range(4):
                    if GPIO.input (ROW[i]) == 0:
                        if MATRIX[i][j] <= 9:
                            ID = ID + str(MATRIX[i][j])
                            print ID
                        elif MATRIX[i][j] == '*':
                            ID = ID[:-1]
                            print ID
                        elif MATRIX[i][j] == '#':
                            url = "http://80026213.ngrok.io/enter/peron_id/" + ID + "/location_id/1"
                            requests.post(url)
                            print ID
			    GPIO.setwarnings(False)
                            GPIO.setup(29,GPIO.OUT)
			    GPIO.output(29,GPIO.HIGH)
		            time.sleep(2)
                            GPIO.output(29,GPIO.LOW)
			    ID = ""
			else:
			    print ("wrong input")
		            GPIO.setup(26,GPIO.OUT)
			    GPIO.output(26,GPIO.HIGH)
                            time.sleep(2)
                            GPIO.output(26,GPIO.LOW)
                        while(GPIO.input(ROW[i]) == 0):
                             pass

            GPIO.output(COL[j],1)
except KeyboardInterrupt:
    GPIO.cleanup()
