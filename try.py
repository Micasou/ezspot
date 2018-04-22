import RPi.GPIO as GPIO
import time
import requests

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

y = ''

while True:
    x = raw_input("type : ")
    if x == '1' or x == '2' or x == '3' or x == '4' or x == '5' or x == '6' or x == '7' or x == '8' or x == '9' or x == '0':
        y = y+x
    elif x == '*':
        y = y[:-1]
    elif x == '$':
        
        GPIO.setup(36,GPIO.OUT)
        GPIO.output(36,GPIO.HIGH)
        time.sleep(2)
        GPIO.output(36,GPIO.LOW)
        url = "http://80026213.ngrok.io/enter/peron_id/" + y + "/location_id/2"
        requests.post(url)
        print (y)
    elif x == '?':
        answer = requests.get("http://80026213.ngrok.io/status/2")
        print (answer.text)
    elif x == '!':
        GPIO.setup(37,GPIO.OUT)
        GPIO.output(37,GPIO.HIGH)
        time.sleep(2)
        GPIO.output(37,GPIO.LOW)
        urlll = "http://80026213.ngrok.io/exit/2"
        response = requests.post(urlll)
        print (response.text)
    else:
        print ('wrong input')
