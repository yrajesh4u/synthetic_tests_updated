import pytest
import json
from pytest_lib import config, add_device_tag, add_mso_tag
from common.base import Base
from pytest_dependency import depends
import time
from synth_test_lib.synthassert import synthassert


@pytest.mark.synthetic_tests_wtwn
@pytest.mark.parametrize('device_domain', config["device_domains"])
class TestWtwn:
    '''
    TITLE: WTWN Multi-Level Validation
    DESCRIPTION:
    Validates that the PCD Discovery endpoints are correctly configured and that all WTWN feeds are working. 
    '''

    base = Base()
    feedItems = {}
    thirdLevelFeedItems = {}

    @staticmethod
    def get_device_config(request, record_xml_attribute, device_domain):
        device_config = config["device_domain_config"][device_domain]
        add_device_tag(
            request=request,
            record_xml_attribute=record_xml_attribute,
            device=device_config['deviceType']
        )
        add_mso_tag(
            request=request,
            record_xml_attribute=record_xml_attribute,
            mso=device_config['mso']
        )
        return device_config

    @pytest.mark.dependency()
    def test_wtwn_root_level(self, device_domain, request, record_xml_attribute, generate_mind_url,
                             generate_json_headers):
        device_domain_config = self.get_device_config(request, record_xml_attribute, device_domain)
        rootfeedname = device_domain_config.get("rootFeedName")
        rootcaption = device_domain_config.get("rootCaption")
        response = self.base.request_api(
            url=generate_mind_url,
            payload=json.dumps(
                self.base.wtwn_payload(device=device_domain_config.get("deviceType"), feedname=rootfeedname,
                                       device_domain_config=device_domain_config)),
            headers=generate_json_headers,
            urlparams={"type": "feedItemFind", "bodyId": device_domain_config.get("bodyId")}
        )
        try:
            json_data = response.json()
            synthassert(
                "caption" in json_data,
                message="Caption attribute missing in response",
                response=response)
            synthassert(
                json_data["caption"] == rootcaption,
                message="Caption attribute value different than:" + str(rootcaption),
                response=response)
            self.base.assert_feeditemfind_response(response)
            synthassert(
                "items" in json_data,
                message="Items attribute not present in response",
                response=response)
            for item in json_data["items"]:
                self.base.assert_feedname_in_response(response, item)
                feedname = item["kernel"]["expandedFeedAction"]["feedName"]
                if feedname == "/liveTvApps":
                    continue
                TestWtwn.feedItems.setdefault(rootcaption, []).append(feedname)
        except ValueError:
            synthassert(False, message="Decoding JSON from the response failed", response=response)

    @pytest.mark.dependency()
    @pytest.mark.flaky(reruns=3)
    def test_wtwn_second_level(self, request, record_xml_attribute, device_domain, generate_mind_url,
                               generate_json_headers):
        depends(request, ["TestWtwn::test_wtwn_root_level[{}]".format(device_domain)])
        device_domain_config = self.get_device_config(request, record_xml_attribute, device_domain)
        rootcaption = device_domain_config.get("rootCaption")
        for feedItem in TestWtwn.feedItems[rootcaption]:
            response = self.base.request_api(
                url=generate_mind_url,
                payload=json.dumps(
                    self.base.wtwn_payload(device=device_domain_config.get("deviceType"), feedname=feedItem,
                                           device_domain_config=device_domain_config)),
                headers=generate_json_headers,
                urlparams={"type": "feedItemFind", "bodyId": device_domain_config.get("bodyId")}
            )
            try:
                json_data = response.json()
                self.base.assert_feeditemfind_response(response)
                synthassert(
                    "items" in json_data,
                    message="Items attribute not present in response",
                    response=response)
                for item in json_data["items"]:
                    self.base.assert_feedname_in_response(response, item)
                    feedname = item["kernel"]["expandedFeedAction"]["feedName"]
                    if feedname == "/liveTvApps":
                        continue
                    TestWtwn.thirdLevelFeedItems.setdefault(rootcaption, []).append(feedname)
            except ValueError:
                synthassert(False, message="Decoding JSON from the response failed", response=response)


    @pytest.mark.dependency()
    @pytest.mark.flaky(reruns=3)
    def test_wtwn_third_level(self, request, record_xml_attribute, device_domain, generate_mind_url,
                              generate_json_headers):
        depends(request, ["TestWtwn::test_wtwn_second_level[{}]".format(device_domain)])
        device_domain_config = self.get_device_config(request, record_xml_attribute, device_domain)
        rootcaption = device_domain_config.get("rootCaption")
        for thirdLevelFeedItem in TestWtwn.thirdLevelFeedItems[rootcaption]:
            time.sleep(1)
            response = self.base.request_api(
                url=generate_mind_url,
                payload=json.dumps(
                    self.base.wtwn_payload(device=device_domain_config.get("deviceType"), feedname=thirdLevelFeedItem,
                                           device_domain_config=device_domain_config)),
                headers=generate_json_headers,
                urlparams={"type": "feedItemFind", "bodyId": device_domain_config.get("bodyId")}
            )
            try:
                self.base.assert_feeditemfind_response(response)
            except ValueError:
                synthassert(False, message="Decoding JSON from the response failed", response=response)
