import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
PIN1 = 14
PIN2 = 15

GPIO.setmode(GPIO.BCM) 

# GPIO 23 & 17 set up as inputs, pulled up to avoid false detection.
# Both ports are wired to connect to GND on button press.
# So we'll be setting up falling edge detection for both
GPIO.setup(PIN1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  
# GPIO 24 set up as an input, pulled down, connected to 3V3 on button press  
# GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  
  
# now we'll define two threaded callback functions  
# these will run in another thread when our events are detected  
def my_callback(channel):  
    print("14")
  
def my_callback2(channel):  
    print("falling edge detected on 15")

# when a falling edge is detected on port 17, regardless of whatever   
# else is happening in the program, the function my_callback will be run  
GPIO.add_event_detect(PIN1, GPIO.FALLING, bouncetime=200)
GPIO.add_event_detect(PIN2, GPIO.FALLING, bouncetime=200)
# when a falling edge is detected on port 23, regardless of whatever   
# else is happening in the program, the function my_callback2 will be run  
# 'bouncetime=300' includes the bounce control written into interrupts2a.py  
#GPIO.add_event_detect(PIN2, GPIO.FALLING, callback=my_callback2, bouncetime=300) 
GPIO.add_event_callback(PIN2, my_callback2)
GPIO.add_event_callback(PIN1, my_callback)
print("Ctrl+C")
while True:
    pass

GPIO.cleanup()
