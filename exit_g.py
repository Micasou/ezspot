import RPi.GPIO as GPIO 
import time
import requests

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
	input_state = GPIO.input(4)
	if input_state == False:
		url = "http://80026213.ngrok.io/exit/1" 
		response = requests.post(url)
		print response.text
		time.sleep(0.2)
