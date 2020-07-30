from flask import Flask
from multiprocessing import Process
import time, datetime
from Sun import Sun

app = Flask(__name__)

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

app = Flask(__name__)

lights = {
    "gardenleft": 37,
    "gardenright": 35,
    "tree": 33
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

SUNSET_DELAY = 0.5
SUNRISE_DELAY = 3

def timingloop():
    coords = {'latitude': 41, 'longitude': -72}
    sun = Sun()
    didsunset = False
    didsunrise = False
    while True:
        sunrise = sun.getSunriseTime(coords)
        sunset = sun.getSunsetTime(coords)
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        hourdec = now.hour + now.minute/60

        sr = (hourdec + SUNRISE_DELAY)%24 > sunrise['decimal']
        if sr and not didsunrise:
            for light in lights.keys():
                setoff(light)
        
        ss = hourdec > (sunset['decimal'] + SUNSET_DELAY)%24
        if ss and not didsunset:
            for light in lights.keys():
                seton(light)

        didsunset, didsunrise = ss, sr

        time.sleep(10)

if __name__ == "__main__":
    p = Process(target=timingloop)
    p.start()
    app.run(debug=True, use_reloader=False)
    p.join()

