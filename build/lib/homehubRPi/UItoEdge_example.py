from httpCommunications import ConnectToAPI
from homehubRPi.mqttCommunications import MQTTClass
import time

if __name__ == "__main__":
    mqttc = MQTTClass()

    # make APIcall and get response forward response to mqtt
    while (True):

        client = ConnectToAPI(
            APIUrl='127.0.0.1:8000', method='GET', data='/devices')
        # client.get_id_and_status(url="http://127.0.0.1:8000/devices/")
        device_state = (client.http_request_get_device(id=1))
        print(type(device_state))

        status = device_state['status']
        print(status)
        # now forward this to edge device
        mqttc.pub(MQTT_BROKER="192.168.1.61",
                MQTT_TOPIC="1", MQTT_PORT=1883, MQTT_MSG=status)
        time.sleep(2)
