
import Adafruit_CharLCD as LCD
import requests
import time
import json
from threading import Timer

lcd_rs        = 25 
lcd_en        = 24
lcd_d4        = 23
lcd_d5        = 17
lcd_d6        = 18
lcd_d7        = 22
lcd_backlight = 4
lcd_columns = 16
lcd_rows = 2


# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows = 2

lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
while True:
	answer = requests.get("http://80026213.ngrok.io/status/1")
	print answer.text
	lcd.message('New Port 1\n'+ answer.text)
	time.sleep(2)
