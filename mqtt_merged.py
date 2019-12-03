import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import sys


MQTT_CHLOE = "192.168.43.1"  # Chloe's IP
MQTT_KAYDEN = "192.168.43.128"  # Kayden's IP
MQTT_JACKY = "192.168.43.138"  # Jacky's IP
MQTT_PATH = "test_channel"

MQTT_CURRENT = MQTT_KAYDEN  # The current user's IP

 
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc: int):
    """
    Print a confirmation message upon successful connection.

    :param client: the device running the script and connecting to the MQTT server
    :param userdata: user data of any type, set when creating the client instance
    :param flags: unused? remove?
    :param rc: int, the result code of the connection.
    :precondition: rc should be 0 if the connection was successful.
    :postcondition: print connection result
    """
    print("Connected with result code "+str(rc))
 
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH)
 
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg: str):
    """
    Publish a message typed by the client to the other devices.

    :param client: the device running the script and connecting to the MQTT server
    :param userdata: user data of any type, set when creating the client instance
    :param msg: string, the message to be sent
    :postcondition: print the message, preceded by the ip
    """

    # client._host is the IP of the client, this distinguishes who sent what message
    # decoding the message with utf-8 helps with formatting and removes quotes/other characters
    print(str(userdata) + ": " + str(msg.payload.decode('utf-8')))


# Set up the client, connect them to the server, allow them to send messages
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.user_data_set(MQTT_CURRENT)

# connect to the current client IP with port 1883 and
# 60 keepalive (the rate ping messages are sent; or max time in seconds allowed between broker communications)
client.connect(MQTT_CURRENT)
 
# Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
client.loop_start()

# publish initial message to server when client connects
publish.single(MQTT_PATH, "The server was opened successfully.", hostname=client._host)

while True:  # continually ask for input to publish
    msg = input()
    for i in [MQTT_CHLOE, MQTT_KAYDEN, MQTT_JACKY]:  # publish message to all 3 devices
        try:
            publish.single(MQTT_PATH, msg, hostname=i)
        except OSError:
            print(i + " is not an open socket.", file=sys.stderr)
