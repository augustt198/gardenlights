from flask import Flask
app = Flask(__name__)

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

lights = {
    "gardenleft": 37,
    "gardenright": 35,
    "tree": None
}

for _, pin in lights.items():
    if pin != None:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, True)

status = {k: False for (k, v) in lights.items()}

@app.route('/status/<light>')
def getstatus(light):
    if light not in lights:
        return "error"

    if status[light]:
        return "1"
    else:
        return "0"

@app.route('/on/<light>')
def seton(light):
    if light not in lights:
        return "error"

    status[light] = True
    pin = lights[light]
    if pin:
        GPIO.output(pin, False)
    return "ok"

@app.route('/off/<light>')
def setoff(light):
    if light not in lights:
        return "error"

    status[light] = False
    pin = lights[light]
    if pin:
        GPIO.output(pin, True)
    return "ok"

