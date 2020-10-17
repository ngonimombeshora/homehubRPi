from homehubRPi.httpCommunications import ConnectToAPI


"""
    This module constantly polls "listens" to the database. to check for change that need to be forwarded to edge devices
    (prompts forwarding of changes using MQTTComms)(Uses httpCommunications module)
    Also listens to edge devices (Uses MQTTCommunications module and prompts database updates)

"""


# Notes
# possible approach: use get_devices from httpComms and temporarily store these values in a dict. Only store "status " to save space.
# Poll and check against previous status
class Listen(object):
    """
    class handling json objects
    """

    def __init__(self, APIUrl, ** kwargs):
        self.APIUrl = APIUrl

    def getStatus(self, id):
        """
        check device status by id, and return status
        """
        client = ConnectToAPI()
        id_and_status_dict = client.get_id_and_status(
            url="http://127.0.0.1:8000/devices/")

        return id_and_status_dict[id]

    def get_id_and_status_dict(self, **kwargs):
        """
        returns a dict of ids and their statuses, to set global varible "previousIDandStatus"
         for "listen_to_user_status_change" to use. `
        """
        client = ConnectToAPI()
        id_and_status_dict = client.get_id_and_status(
            url="http://127.0.0.1:8000/devices/")

        return id_and_status_dict

    def dict_compare(self, d1, d2):
        """
        compare value in two dictinaries
        """
        d1_keys = set(d1.keys())
        d2_keys = set(d2.keys())
        shared_keys = d1_keys.intersection(d2_keys)
        added = d1_keys - d2_keys
        removed = d2_keys - d1_keys
        modified = {o: (d1[o], d2[o]) for o in shared_keys if d1[o] != d2[o]}
        same = set(o for o in shared_keys if d1[o] == d2[o])
        return added, removed, modified, same

    def listen_to_user_status_change(self, listenRate=None, previousIDandStatusDict=dict, **kwargs):
        """
        Indefinately listens to database, waiting for status changes
        promts mqttComms function to forward status to edge device
        """

        client = ConnectToAPI()

        id_and_status_dict = client.get_id_and_status(
            url="http://127.0.0.1:8000/devices/")
        # compare statuses from previous time to now
        added, removed, modified, same = self.dict_compare(id_and_status_dict,
                                                           previousIDandStatusDict)
        return same
