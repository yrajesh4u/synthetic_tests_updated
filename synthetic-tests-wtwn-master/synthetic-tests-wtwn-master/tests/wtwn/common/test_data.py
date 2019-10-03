from pytest_lib import config

class TestDataWhatToWatch:
    """
    This class is inherited by base.py::Base

    Contains test data used by wtwn synthetic test endpoints.
    """

    @staticmethod
    def wtwn_payload(device='androidTv',feedname=None, device_domain_config=None):
        payload = {
          "displayCount": config["displayCount"],
          "type": "feedItemFind",
          "bodyId": device_domain_config["bodyId"],
          "deviceType": device,
          "displayType": "quick",
          "feedName": feedname
        }
        return payload