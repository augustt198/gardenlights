import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

import sys
import time

pin = int(sys.argv[1])
GPIO.setup(pin, GPIO.OUT)
print("Turning pin %d on" % pin)
GPIO.output(pin, True)
time.sleep(4)
GPIO.output(pin, False)
time.sleep(0.5)
