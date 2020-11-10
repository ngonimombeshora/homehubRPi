from homehubRPi.mqttCommunications import MQTTClass


if __name__ == "__main__":
    mqttc = MQTTClass()

    rc = mqttc.run(MQTT_BROKER="192.168.1.61",
                MQTT_TOPIC="1", MQTT_PORT=1883)
    # mqttc.pub("192.168.1.61", "helloTopic", "hello_message")

    print("rc:"+str(rc))
