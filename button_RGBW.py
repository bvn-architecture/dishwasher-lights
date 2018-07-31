import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time
from neopixel import *

# Use BCM pin numbering
GPIO.setmode(GPIO.BCM) 
PIN1 = 14
PIN2 = 15
# 200 ms debounce cutoff 
debounce_thresh = 200 
GPIO.setmode(GPIO.BCM)
# Set pins be input pins and set initial values to be pulled HIGH (ON)
GPIO.setup(PIN1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# setup RGBW LEDS
LED_COUNT      = 180      # Number of LED pixels.
LED_PIN        = 21      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0
LED_STRIP      = ws.SK6812_STRIP_RGBW

LEFT_FLAG = None
LEFT_FLAG = None


def press_left(channel):
    """Callback for left dishwasher"""
    
    global LEFT_FLAG
    if LEFT_FLAG == 0:
        color = Color(128, 0,0, 0)
    elif LEFT_FLAG == 1:
        color = Color(0, 128, 0, 0)
    elif LEFT_FLAG == 2:
        color = Color(0, 0, 128, 0)
    print("LEFT button: {}".format(color))
    for i in range(0,60):
        strip.setPixelColor(i, color)
    strip.show()
    LEFT_FLAG = (LEFT_FLAG + 1) % 3


def press_right(channel):
    """Callback for right dishwasher"""
    global RIGHT_FLAG
    if RIGHT_FLAG == 0:
        color = Color(128,0,0, 0)
    elif RIGHT_FLAG == 1:
        color = Color(0, 128, 0, 0)
    elif RIGHT_FLAG == 2:
        color = Color(0, 0, 128, 0)
    rint("RIGHT button: {}".format(color))
    for i in range(120, strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()
    RIGHT_FLAG = (RIGHT_FLAG + 1) % 3


# Main program logic follows:
# if __name__ == '__main__':
# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ,
	                          LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
# Intialize the library (must be called once before other functions).
strip.begin()
LEFT_FLAG = 0
RIGHT_FLAG = 0
color = (0,0,0,0)
GPIO.add_event_detect(PIN1, GPIO.FALLING, bouncetime=debounce_thresh)
GPIO.add_event_detect(PIN2, GPIO.FALLING, bouncetime=debounce_thresh)

GPIO.add_event_callback(PIN2, press_left)
GPIO.add_event_callback(PIN1, press_right)

print('Press Ctrl-C to quit.')
while True:
	pass

GPIO.cleanup()

