import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time
from neopixel import *
from basicPubSub import myAWSIoTMQTTClient
import json
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



def press_left(channel):
    """Callback for left dishwasher"""
    global LEFT_FLAG, COUNTER
    message = {}
    # if command == "g":
    message['dishwasher'] = 'left'
    message['sequence'] = COUNTER
    if LEFT_FLAG == 0:
        message['message'] = 'running'
        color = Color(128, 0,0, 0)
    elif LEFT_FLAG == 1:
        message['message'] = 'loading_dishes'
        color = Color(0, 128, 0, 0)
    elif LEFT_FLAG == 2:
        message['message'] = 'lights_off'
        color = Color(0, 0, 128, 0)
    print("LEFT button: {}".format(color))
    for i in range(0,60):
        strip.setPixelColor(i, color)
    strip.show()
    LEFT_FLAG = (LEFT_FLAG + 1) % 3


def press_right(channel):
    """Callback for right dishwasher"""
    global RIGHT_FLAG, COUNTER
    message = {} 
    message['dishwasher'] = 'right'
    message['sequence'] = COUNTER
    if RIGHT_FLAG == 0:
        message['message'] = 'running'
        color = Color(128,0,0, 0)
    elif RIGHT_FLAG == 1:
        message['message'] = 'loading_dishes'
        color = Color(0, 128, 0, 0)
    elif RIGHT_FLAG == 2:
        message['message'] = 'lights_off'
        color = Color(0, 0, 128, 0)
    print("RIGHT button: {}".format(color))
    for i in range(120, strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()
    RIGHT_FLAG = (RIGHT_FLAG + 1) % 3


# Main program logic follows:
if __name__ == '__main__':

    AllowedActions = ['both', 'publish', 'subscribe']

    # Custom MQTT message callback
    def customCallback(client, userdata, message):
        print("Received a new message: ")
        print(message.payload)
        print("from topic: ")
        print(message.topic)
        print("--------------\n\n")


    # Read in command-line parameters
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--endpoint", action="store", required=True, dest="host", help="Your AWS IoT custom endpoint")
    parser.add_argument("-r", "--rootCA", action="store", required=True, dest="rootCAPath", help="Root CA file path")
    parser.add_argument("-c", "--cert", action="store", dest="certificatePath", help="Certificate file path")
    parser.add_argument("-k", "--key", action="store", dest="privateKeyPath", help="Private key file path")
    parser.add_argument("-p", "--port", action="store", dest="port", type=int, help="Port number override")
    parser.add_argument("-w", "--websocket", action="store_true", dest="useWebsocket", default=False,
                        help="Use MQTT over WebSocket")
    parser.add_argument("-id", "--clientId", action="store", dest="clientId", default="basicPubSub",
                        help="Targeted client id")
    parser.add_argument("-t", "--topic", action="store", dest="topic", default="dishwasher_button", help="Targeted topic")
    parser.add_argument("-m", "--mode", action="store", dest="mode", default="both",
                        help="Operation modes: %s"%str(AllowedActions))
    parser.add_argument("-M", "--message", action="store", dest="message", default="Hello World!",
                        help="Message to publish")

    args = parser.parse_args()
    host = args.host
    rootCAPath = args.rootCAPath
    certificatePath = args.certificatePath
    privateKeyPath = args.privateKeyPath
    port = args.port
    useWebsocket = args.useWebsocket
    clientId = args.clientId
    topic = args.topic

    if args.mode not in AllowedActions:
        parser.error("Unknown --mode option %s. Must be one of %s" % (args.mode, str(AllowedActions)))
        exit(2)

    if args.useWebsocket and args.certificatePath and args.privateKeyPath:
        parser.error("X.509 cert authentication and WebSocket are mutual exclusive. Please pick one.")
        exit(2)

    if not args.useWebsocket and (not args.certificatePath or not args.privateKeyPath):
        parser.error("Missing credentials for authentication.")
        exit(2)

    # Port defaults
    if args.useWebsocket and not args.port:  # When no port override for WebSocket, default to 443
        port = 443
    if not args.useWebsocket and not args.port:  # When no port override for non-WebSocket, default to 8883
        port = 8883

    # Configure logging
    logger = logging.getLogger("AWSIoTPythonSDK.core")
    logger.setLevel(logging.DEBUG)
    streamHandler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)

    # Init AWSIoTMQTTClient
    myAWSIoTMQTTClient = None
    if useWebsocket:
        myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId, useWebsocket=True)
        myAWSIoTMQTTClient.configureEndpoint(host, port)
        myAWSIoTMQTTClient.configureCredentials(rootCAPath)
    else:
        myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
        myAWSIoTMQTTClient.configureEndpoint(host, port)
        myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

    # AWSIoTMQTTClient connection configuration
    myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
    myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
    myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
    myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
    myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

    # Connect and subscribe to AWS IoT
    myAWSIoTMQTTClient.connect()
    # if args.mode == 'both' or args.mode == 'subscribe':
    #     myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)
    time.sleep(2)

    # hardware code Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ,
                            LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    LEFT_FLAG = 0
    RIGHT_FLAG = 0
    COUNTER = 0
    color = (0,0,0,0)
    GPIO.add_event_detect(PIN1, GPIO.FALLING, bouncetime=debounce_thresh)
    GPIO.add_event_detect(PIN2, GPIO.FALLING, bouncetime=debounce_thresh)

    GPIO.add_event_callback(PIN2, press_left, myAWSIoTMQTTClient)
    GPIO.add_event_callback(PIN1, press_right, myAWSIoTMQTTClient)

    print('Press Ctrl-C to quit.')
    while True:
        pass

    GPIO.cleanup()
