import paho.mqtt.publish as publish
 
MQTT_SERVER = "142.232.155.59" # IP of other pi
MQTT_PATH = "test_channel"
 
publish.single(MQTT_PATH, "Hello World!", hostname=MQTT_SERVER)

while True:
    msg = input()
    publish.single(MQTT_PATH, msg, hostname=MQTT_SERVER)