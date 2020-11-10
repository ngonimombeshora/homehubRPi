# Import package
# import context  # Ensures paho is in PYTHONPATH
import paho.mqtt.client as mqtt


if __name__ == "__main__":
    # Define Variables
    MQTT_HOST = "192.168.1.61"
    MQTT_PORT = 1883
    MQTT_KEEPALIVE_INTERVAL = 45
    MQTT_TOPIC = "1"
    MQTT_MSG = str("hello MQTT _1")


    # Define on_publish event function
    def on_publish(client, userdata, mid):
        print("Message Published...")


    # Initiate MQTT Client
    mqttc = mqtt.Client()

    # Register publish callback function
    mqttc.on_publish = on_publish

    # Connect with MQTT Broker
    mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)

    # Publish message to MQTT Broker
    # while True:
    mqttc.publish(MQTT_TOPIC, MQTT_MSG)

    # Disconnect from MQTT_Broker
    mqttc.disconnect()
