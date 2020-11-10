import http.client
import json
import requests


class ConnectToAPI(object):
    """
    Connect to hup_api via http. Enables access and control to database.
    """

    def __init__(self, APIUrl=None, method=None, data=None, headers=None, id=int, ** kwargs):
        self.APIUrl = APIUrl
        self.method = method
        self.data = data
        self.headers = headers

    def http_request_get(self, **kwargs):
        """
            Make an HTTP request to the API and return list of devices.
        """
        conn = http.client.HTTPConnection(self.APIUrl)

        conn.request("GET", "/devices/")

        res = conn.getresponse()
        data = res.read()

        print(data.decode("utf-8"))
        return data

    def http_request_get_device(self, id=None, **kwargs):
        """
            Make an HTTP request to the API and return specific device information based on the device "id".
        """

        conn = http.client.HTTPConnection(self.APIUrl)
        payload = ""

        headers = {
            'cookie': "csrftoken=Htxdl0KSxalzvXlthtOnPYkM9xFSb17I8wBgh0xTAVn5S7CXiVU2CD2tOZlFTZes",
            'Content-Type': "application/json",
            'Authorization': "Basic UGFyZW50OnBhJCR3b3JkMTIz"
        }

        conn.request("GET", "/devices/{}/".format(id), payload, headers)

        res = conn.getresponse()
        data = json.loads(res.read())  # .decode("utf-8")

        # print(data.decode("utf-8"))
        return data

    def http_post(self, name=None, category=None, location=None, device_id=None, status=None, jsonData=None, **kwargs):
        """
            Make an HTTP post to the hub_api. Used to add a device to the database.
        """
        conn = http.client.HTTPConnection(self.APIUrl)

        # convert data to json
        payloadDict = {
            "name": "{}".format(name),
            "category": category,
            "location": location,
            "device_id": device_id,
            "status": status
        }

        if jsonData:
            jsonToHttp = json.dumps(jsonData)
        else:
            jsonToHttp = json.dumps(payloadDict)

        headers = {
            'cookie': "csrftoken=Htxdl0KSxalzvXlthtOnPYkM9xFSb17I8wBgh0xTAVn5S7CXiVU2CD2tOZlFTZes",
            'content-type': "application/json",
            'authorization': "Basic dGVzdHVzZXIxOnBhJCR3b3JkMTIz"
        }

        conn.request("POST", "/devices/", jsonToHttp, headers)

        res = conn.getresponse()
        data = res.read()

        print(data.decode("utf-8"))
        return data

    def http_put(self, id=None, name=None, category=None, location=None, device_id=None, status=None, jsonData=None, **args):
        """
            Make an HTTP PUT request to the API . Normally used to update device,
            Especially changing states, "ON" and "OFF",
            Or update device details
            N.B To make a put get the device ID number from devices list
        """
        conn = http.client.HTTPConnection(self.APIUrl)
        headers = {
            'cookie': "csrftoken=Htxdl0KSxalzvXlthtOnPYkM9xFSb17I8wBgh0xTAVn5S7CXiVU2CD2tOZlFTZes",
            'content-type': "application/json",
            'authorization': "Basic UGFyZW50OnBhJCR3b3JkMTIz"
        }
        # convert data to json
        # "PUT" method from harware api should only alter "status" and "reading" fields
        payloadDict = {
            "name": "",
            "category": "",
            "location": "",
            "device_id": device_id,
            "status": str(status)
        }
        if jsonData:
            jsonToHttp = json.dumps(jsonData)
        else:
            jsonToHttps = json.dumps(payloadDict)
            # payload = "{\n\t\"status\":\"{}\"\n}".format(str(status))
            # conn.request("PUT", "/devices/{}/".format(id), payload, headers)

        # payload = "{\n\t\"name\": \"test permissions\",\n\t\"category\": \"sensor\",\n\t\"location\": \"\",\n\t\"device_id\": \"\",\n\t\"status\": \"ON\",\n\t\"created\": \"2020-10-05T19:31:38.548243Z\"\n}"

        conn.request("PUT", "/devices/{}/".format(id), jsonData, headers)

        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))
        return data

    def http_delete(self, id=None):  # ToDo confirm user authentication for deleting
        """
            Select the device "id" you want to delete not "device_id"
            N.B get "id" from devices list
        """
        conn = http.client.HTTPConnection(self.APIUrl)

        # payload = "{\n\t\"name\": \"test permissions\",\n\t\"category\": \"sensor\",\n\t\"location\": \"\",\n\t\"device_id\": \"\",\n\t\"status\": \"ON\",\n\t\"created\": \"2020-10-05T19:31:38.548243Z\"\n}"
        payload = ""
        headers = {
            'cookie': "csrftoken=Htxdl0KSxalzvXlthtOnPYkM9xFSb17I8wBgh0xTAVn5S7CXiVU2CD2tOZlFTZes",
            'content-type': "application/json",
            'authorization': "Basic YWRtaW46cGFzc3dvcmQxMjM="
        }

        conn.request("DELETE", "/devices/{}/".format(id), payload, headers)

        res = conn.getresponse()
        data = res.read()

        print(data.decode("utf-8"))
        return data

    def get_id_and_status(self, url=None, **kwargs):
        """
            fetch id and status of devices from the database
        """

        payload = "curl --request GET \\\n  --url {url} \\\n  --header 'authorization: Basic YWRtaW5zOnBhc3N3b3JkMTIz' \\\n  --header 'content-type: application/json' \\\n  --cookie csrftoken=Htxdl0KSxalzvXlthtOnPYkM9xFSb17I8wBgh0xTAVn5S7CXiVU2CD2tOZlFTZes"
        headers = {
            'cookie': "csrftoken=Htxdl0KSxalzvXlthtOnPYkM9xFSb17I8wBgh0xTAVn5S7CXiVU2CD2tOZlFTZes",
            'content-type': "application/json",
            'authorization': "Basic YWRtaW46cGFzc3dvcmQxMjM="
        }

        response = requests.request("GET", url, data=payload, headers=headers)
        data = response.json()
        devices = data["results"]
        # create an id and status dict
        id_and_staus_dict = {}

        for device in devices:
            id_and_staus_dict[device["id"]] = device["status"]

        return id_and_staus_dict

# N.B in terminal http://admin:password123@127.0.0.1:8000/devices/...
