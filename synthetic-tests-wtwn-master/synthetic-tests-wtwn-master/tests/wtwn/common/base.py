import requests
from common.test_data import TestDataWhatToWatch
from pytest_lib import config
from synth_test_lib.synthassert import synthassert

class Base(TestDataWhatToWatch):
    """
    This class is to request api & assert the response.
    """

    @staticmethod
    def request_api(url, payload=None, method="POST",headers=None,urlparams=None, **kwargs):
        """
        This method is to post/get request and return response in dict format.
        :param url: request url
        :param payload: request payload
        :param method: type of method (POST and GET Supported)
        :param kwargs: kwargs to pass other params like timeout,auth,cert
        :return: dict of response
        """

        if method == "POST":
            resp = requests.post(
                url=url,
                data=payload,
                headers=headers,
                params=urlparams,
                **kwargs
            )
        else:
            resp = requests.get(url=url, headers=headers,params=urlparams, **kwargs)

        synthassert(
            resp.status_code == 200,
            message="status code mismatched",
            response=resp
        )
        return resp

    @staticmethod
    def assert_feeditemfind_response(response):
        """
        This method validates some fields on response of feedItemFind api
        :param response: feedItemFind api response as response object
        :return: None
        """

        json_data = response.json()
        synthassert(
            "type" in json_data,
            message="Type attribute missing in response!",
            response=response)
        synthassert(
            json_data["type"] == "feedItemResults",
            message="Type attribute value is not feedItemResults in response",
            response=response)
        synthassert(
            "feedItemFindCallId" in json_data,
            message="feedItemFindCallId attribute missing in response!",
            response=response)
        synthassert(
            json_data["feedItemFindCallId"] != "dummyQueryId",
            message="feedItemFindCallId attribute value is dummyQueryId",
            response=response)

    @staticmethod
    def assert_feedname_in_response(response, response_item):
        """
        This method checks the existence of feedname attribute in an item in response passed
        :param response: feedItemFind api response as response object
        :param response_item: individual item in response
        :return: None
        """

        synthassert(
            "kernel" in response_item,
            message="Missing kernel attribute in response.",
            response=response)
        synthassert(
            "expandedFeedAction" in response_item["kernel"],
            message="Missing expandedFeedAction attribute in response.",
            response=response)
        synthassert(
            "feedName" in response_item["kernel"]["expandedFeedAction"],
            message="Missing feedName attribute in response.",
            response=response)

