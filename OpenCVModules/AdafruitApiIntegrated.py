
# Import standard python modules.
import sys
from picamera import PiCamera

camera = PiCamera()

# Import Adafruit IO MQTT client.
from Adafruit_IO import MQTTClient


# Set to your Adafruit IO key & username below.
ADAFRUIT_IO_KEY      = 'aio_NoVO48Fm2hGfwkvXYdfcqrMF8VIy' 
ADAFRUIT_IO_USERNAME = 'PranavViswanathan'  # See https://accounts.adafruit.com
                                                    # to find your username.

# Set to the ID of the feed to subscribe to for updates.
FEED_ID = 'Take Image'

cnt = 0
# Define callback functions which will be called when certain events happen.
def connected(client):
    # Connected function will be called when the client is connected to Adafruit IO.
    # This is a good place to subscribe to feed changes.  The client parameter
    # passed to this function is the Adafruit IO MQTT client so you can make
    # calls against it easily.
    print('Connected to Adafruit IO!  Listening for {0} changes...'.format(FEED_ID))
    # Subscribe to changes on a feed named DemoFeed.
    client.subscribe(FEED_ID)

def disconnected(client):
    # Disconnected function will be called when the client disconnects.
    print('Disconnected from Adafruit IO!')
    sys.exit(1)

def message(client, feed_id, payload):
    # Message function will be called when a subscribed feed has a new value.
    # The feed_id parameter identifies the feed, and the payload parameter has
    # the new value.
    global cnt
    print('Feed {0} received new value: {1}'.format(feed_id, payload))
    if payload=='Cam On':
        camera.capture("/home/pi/Desktop/Images/image{}.jpg".format(cnt))
        cnt = (cnt) + 1
        print(cnt)
    elif payload=='Cam Off':
         print("Off")
    
        


# Create an MQTT client instance.
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Setup the callback functions defined above.
client.on_connect    = connected
client.on_disconnect = disconnected
client.on_message    = message

# Connect to the Adafruit IO server.
client.connect()

# Start a message loop that blocks forever waiting for MQTT messages to be
# received.  Note there are other options for running the event loop like doing
# so in a background thread--see the mqtt_client.py example to learn more.
client.loop_blocking()
