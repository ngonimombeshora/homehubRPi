from homehubRPi.httpCommunications import ConnectToAPI
from homehubRPi.Listen import Listen
from homehubRPi.mqttCommunications import MQTTClass
# ------------------------------------
# start testing comms module
# ----------------------------------------

# Ensure that the server is running
# TEst command: python3 -m pytest tests/test.py  "-m flag ensures path is improted to resolve immports"


# def test_http_request_view_devices():
#     client = ConnectToAPI(
#         APIUrl='127.0.0.1:8000', method='GET', data='/devices')
#     print(len(client.http_request_get()))


# def test_http_post():  # test for users currently running test user1
#     client = ConnectToAPI(
#         APIUrl='127.0.0.1:8000', method='GET', data='/devices')

#     # create test data
#     name = 'pypi test module'
#     category = 'PyPI device'
#     location = 'test script'
#     device_id = ""
#     status = "OFF"

#     dummyData = {
#         "name": "{}".format(name),
#         "category": "{}".format(category),
#         "location": "{}".format(location),
#         "device_id": "{}".format(device_id),
#         "status": "{}".format(status)
#     }
#     # client.http_post(name='pypi test module', category='PyPI deviceS',
#     #                  location='test script', device_id="", status='OFF')
#     client.http_post(jsonData=dummyData)
#     print(client.data)


# def test_http_put():
#     client = ConnectToAPI(
#         APIUrl='127.0.0.1:8000', method='GET', data='/devices')

#     # create test data
#     name = 'pypi test module'
#     category = 'PyPI device'
#     location = 'test script'
#     device_id = ""
#     status = "OFF"

#     dummyData = {
#         "name": "{}".format(name),
#         "category": "{}".format(category),
#         "location": "{}".format(location),
#         "device_id": "{}".format(device_id),
#         "status": "{}".format(status)
#     }

#     client.http_put(
#         id="4", jsonData=dummyData)
#     # assert client.http_put(
#     #     id="4", jsonData=dummyData) == "{'detail': 'You do not have permission to perform this action.'}"
#     print(client.data)


# def test_http_delete():
#     client = ConnectToAPI(
#         APIUrl='127.0.0.1:8000', method='GET', data='/devices')

#     client.http_delete(id=4)
#     # assert client.http_put(
#     #     id="4", jsonData=dummyData) == "{'detail': 'You do not have permission to perform this action.'}"
#     print(client.data)


# def test_http_request_get_device():
#     client = ConnectToAPI(
#         APIUrl='127.0.0.1:8000', method='GET', data='/devices')
#     client.http_request_get_device(id=5)


# def test_get_id_and_status():

#     client = ConnectToAPI(
#         APIUrl='127.0.0.1:8000', method='GET', data='/devices')
#     client.get_id_and_status(url="http://127.0.0.1:8000/devices/")

# # _____________________________________________________________________________
# # _________________________test listen module__________________________________


# # def test_get_id_and_status_dict():
# #     listen = Listen(APIUrl="http://127.0.0.1:8000/devices/")


# def test_listen_to_user_status_change():
#     client = ConnectToAPI(
#         APIUrl='127.0.0.1:8000', method='GET', data='/devices')
#     client.get_id_and_status(url="http://127.0.0.1:8000/devices/")

#     listen = Listen(APIUrl="http://127.0.0.1:8000/devices/")

#     previousIDandStatusDict = client.get_id_and_status(
#         url="http://127.0.0.1:8000/devices/")

#     # modify a device status to check if its picked up
#     # previousIDandStatusDict = listen.get_id_and_status_dict
#     print(listen.listen_to_user_status_change(
#         previousIDandStatusDict=previousIDandStatusDict))

def test_mqtt_client():
    mqttc = MQTTClass()
    rc = mqttc.run("192.168.1.61", "helloTopic")
    # mqttc.pub("192.168.1.61", "helloTopic", "hello_message")

    print("rc:"+str(rc))
