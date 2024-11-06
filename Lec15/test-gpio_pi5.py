import time
from gpiozero import DigitalOutputDevice
relay = DigitalOutputDevice(4, active_high=False)
relay.on()
time.sleep(10)
