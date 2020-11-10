#!/usr/bin/python
# -*- coding: utf-8 -*-

# Using the MQTT client in a class.

# import context  # Ensures paho is in PYTHONPATH
import paho.mqtt.client as mqtt
from homehubRPi.httpCommunications import ConnectToAPI


class MQTTClass(mqtt.Client):
    '''
    MQTT client class. All paho-mqtt functions available
    '''

    def on_connect(self, mqttc, obj, flags, rc):
        print("rc: "+str(rc))

    def on_message(self, mqttc, obj, msg):
        client = ConnectToAPI(
            APIUrl='127.0.0.1:8000', data='/devices')
        client.http_put(id=msg.topic, jsonData=(msg.payload).decode("utf-8"))
        # covert type b' to string
        print(msg.topic+" "+str(msg.qos)+" "+(msg.payload).decode("utf-8"))

    def on_publish(self, mqttc, obj, mid):
        print("mid: "+str(mid))
        print("Published")

    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        print("Subscribed: "+str(mid)+" "+str(granted_qos))

    def on_log(self, mqttc, obj, level, string):
        print(string)

    def run(self, MQTT_BROKER, MQTT_PORT, MQTT_TOPIC, **kwargs):
        self.connect(MQTT_BROKER, MQTT_PORT, 60)
        self.subscribe(MQTT_TOPIC, 0)
        rc = 0
        while rc == 0:
            rc = self.loop()
        return rc

    def pub(self, MQTT_BROKER, MQTT_PORT, MQTT_TOPIC, MQTT_MSG, **kwargs):
        self.connect(MQTT_BROKER, 1883, 60)
        self.publish(MQTT_TOPIC, MQTT_MSG)


# If you want to use a specific client id, use
# mqttc = MyMQTTClass("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.
