import time
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
# GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM) # Use physical pin numbering
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 16 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
"""while True: # Run forever
    if GPIO.input(16) == GPIO.HIGH:
        print("Button1")
    elif GPIO.input(26) == GPIO.HIGH:
	print("Button2")
"""
def left_button(channel):
    print("left", channel)

GPIO.add_event_detect(16, GPIO.FALLING, callback=left_button,bouncetime=700)
while True:
    pass
