import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt


MQTT_CHLOE = "192.168.43.106"  # Chloe's IP
MQTT_KAYDEN = "192.168.43.12"  # Kayden's IP
MQTT_JACKY = "192.168.43.142"  # Jacky's IP
MQTT_PATH = "test_channel"

MQTT_CURRENT = MQTT_KAYDEN  # The current user's IP

 
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc: int):  # middle 2 params are unused, will it break if they are removed?
    """
    Print a confirmation message upon successful connection.

    :param client:
    :param userdata: unused? remove?
    :param flags: unused? remove?
    :param rc: int, the result code of the connection.
    :precondition: rc should be 0 if the connection was successful.
    :return: none, uses print statement.
    """
    print("Connected with result code "+str(rc))
 
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH)
 
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(str(client._host) + ": " + str(msg.payload.decode('utf-8')))
    # more callbacks, etc
 
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
 
client.connect(MQTT_CURRENT, 1883, 60)
 
# Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
client.loop_start()

# publish initial message to server when client connects
publish.single(MQTT_PATH, "The server was opened successfully.", hostname=client._host)

while True:  # continually ask for input to publish
    msg = input()
    for i in [MQTT_CHLOE, MQTT_KAYDEN, MQTT_JACKY]:  # publish message to all 3 devices
        publish.single(MQTT_PATH, msg, hostname=i)
