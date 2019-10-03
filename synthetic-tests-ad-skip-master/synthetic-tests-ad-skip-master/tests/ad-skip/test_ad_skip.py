import json
import sys
import time
import requests
import pytest
import conftest
from adSkipPayloads import adSkipPayloads
from checkJson import check_ignore_missing
from pytest_lib import config, mso_tag
from synth_test_lib.synthassert import synthassert

@pytest.mark.parametrize('mso', ['common'])
@pytest.mark.usefixtures("mso_tag")

class Testadskip:
    payloads = adSkipPayloads()
    previousTestPassed = False # used so that test dependencies will be skipped if an earlier test failed.

    def test_clipMetatdataStore(self, setup_content, generate_middleMind_url,
                                generate_default_headers, generate_clipMetadataStore_params, expected_clipMetadataStore):
        contentId = setup_content
        if contentId == None:
            pytest.skip('\nTest Depencency Issue'
                        "\nCouldn't store content object")
        payload = self.payloads.payload_clipMetadataStore(contentId)
        response = requests.post(generate_middleMind_url, headers=generate_default_headers, params=generate_clipMetadataStore_params, data=payload)
        synthassert(response.status_code == 200,
                    message="Status code error\nExpected:  '{}'\nActual:  '{}'\nReason:  '{}'".format(
                        200, response.status_code, response.reason),
                    response=response)
        
        try:
            json_data = response.json()
            synthassert(check_ignore_missing(json_data, expected_clipMetadataStore),
                        message="Returned JSON has incorrect data\nExpected:  '{}'\nActual:  '{}'".format(
                            expected_clipMetadataStore, json_data),
                            response=response)
                        
            
        except json.JSONDecodeError:
            synthassert(False, message="Decoding JSON from the response failed", response=response)
        except KeyError as e:
            synthassert(False,
                        message="Missing key while parsing the json response. Details:" + str(e),
                        response=response)
        Testadskip.previousTestPassed = True
    
    def test_clipMetadataSearch(self, setup_content, generate_middleMind_url, generate_clipMetadataSearch_params,
                                generate_default_headers, expected_clipMetadataSearch):
        contentId=setup_content
        
        if contentId == None or not Testadskip.previousTestPassed:
            pytest.skip('\nTest Depencency Issue'
                        "\nCouldn't store content object or clipMetadataStore failed")

        payload = self.payloads.payload_clipMetadataSearch(contentId)
        maxLoops = config["maxLoops"]
        delay = config["delay"]
        success = False
        loops = 0

        while not success:
            response = requests.post(generate_middleMind_url, headers=generate_default_headers, params=generate_clipMetadataSearch_params, data=payload)
            synthassert(response.status_code == 200,
                        message="Status code error\nExpected:  '{}'\nActual:  '{}'\nReason:  '{}'".format(
                            200, response.status_code, response.reason),
                        response=response)
            

            json_data = response.json()
            if "clipMetadata" in json_data:
                success = check_ignore_missing(json_data['clipMetadata'][0], expected_clipMetadataSearch)
                if success:
                    break
            else:
                loops+=1
                if loops == maxLoops:
                    break
                else:
                    time.sleep(delay)

        synthassert(success, message="Returned JSON has incorrect data\nExpected:  '{}'\nActual:  '{}'".format(
                                expected_clipMetadataSearch, json_data),
                                response=response)
                                
    def test_clipMetadataRemove(self, setup_content, generate_middleMind_url,
                                generate_default_headers, generate_clipMetadataRemove_params):
        contentId=setup_content
        if contentId == None or not Testadskip.previousTestPassed:
            pytest.skip('\nTest Depencency Issue'
                        "\nCouldn't store content object or clipMetadataStore failed")

        Testadskip.previousTestPassed = False
        payload = self.payloads.payload_clipMetadataRemove()
        response = requests.post(generate_middleMind_url, headers=generate_default_headers, params=generate_clipMetadataRemove_params, data=payload)
        synthassert(response.status_code == 200,
                    message="Status code error\nExpected:  '{}'\nActual:  '{}'\nReason:  '{}'".format(
                        200, response.status_code, response.reason),
                    response=response)
        
        try:
            json_data = response.json()
            synthassert("success" == json_data["type"],
                        message="Returned JSON has incorrect data\nExpected:  'success'\nActual:  '{}'".format(json_data),
                        response=response)
        
        except json.JSONDecodeError:
            synthassert(False, message="Decoding JSON from the response failed", response=response)
        except KeyError as e:
            synthassert(False,
                        message="Missing key while parsing the json response. Details:" + str(e),
                        response=response)
        
        Testadskip.previousTestPassed = True
    
    def test_clipMetadataSearch_AfterRemove(self, setup_content, generate_middleMind_url, generate_clipMetadataSearch_params,
                                generate_default_headers):
        contentId=setup_content
        if contentId == None or not Testadskip.previousTestPassed:
            pytest.skip('\nTest Depencency Issue'
                        "\nCouldn't store content object or either clipMetadataStore or clipMetadataRemove failed")

        payload = self.payloads.payload_clipMetadataSearch(contentId)
        response = requests.post(generate_middleMind_url, headers=generate_default_headers, params=generate_clipMetadataSearch_params, data=payload)
        maxLoops = config["maxLoops"]
        delay = config["delay"]
        success = False
        loops = 0

        while not success:
            response = requests.post(generate_middleMind_url, headers=generate_default_headers, params=generate_clipMetadataSearch_params, data=payload)
            synthassert(response.status_code == 200,
                        message="Status code error\nExpected:  '{}'\nActual:  '{}'\nReason:  '{}'".format(
                            200, response.status_code, response.reason),
                        response=response)
            

            json_data = response.json()
            if "clipMetadata" in json_data:
                success = True == json_data["clipMetadata"][0]["isRevoked"]
                if success:
                    break
            else:
                loops+=1
                if loops == maxLoops:
                    break
                else:
                    time.sleep(delay)

        synthassert(success, message="Returned JSON has incorrect data\nExpected:  isRevoked to be True, but is False",
                                response=response)