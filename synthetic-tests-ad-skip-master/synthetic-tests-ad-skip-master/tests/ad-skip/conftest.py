import pytest
import json
import requests
from pytest_lib import config
from synth_test_lib.synthassert import synthassert

"""

URL SECTION

"""
@pytest.fixture(scope="session")
def generate_middleMind_url():
    """
    This fixture generates the middleMind url by using data from the target yaml file
    """
    return 'http://' + config['mm_url'] + ':' + config['mm_port']+config['mind_version']

@pytest.fixture(scope="session")
def generate_appserver_url():

    """
    This fixture generates the appserver url by using data from the target yaml file
    """
    return 'http://' + config['as_url'] + ':' + config['as_port']+config['mind_version']

                

"""
    
    Default Header
    
"""

@pytest.fixture(scope="session")
def generate_default_headers():
    """
        This fixture generates default headers used by ad skip api requests.
    """
    return  {"Content-Type":"application/json","Accept":"application/json", "ApplicationName":"SyntheticTests", "ApplicationFeatureArea":"AdSkip"}

"""

Params Section

"""

@pytest.fixture(scope="session")
def generate_clipMetadataStore_params():
    """
    This fixture generates clipMetadataStore params used by ad skip api requests
    """

    return{"type":"clipMetadataStore"}

@pytest.fixture(scope="session")
def generate_clipMetadataSearch_params():
    """
    This fixture generates clipMetadataSearch params used by ad skip api requests
    """

    return{"type":"clipMetadataSearch"}

@pytest.fixture(scope="session")
def generate_clipMetadataStateGet_params():
    """
    this fixture generates clipMetadataStateGet params used by ad skip api requests
    """

    return{"type":"clipMetadataStateGet"}

@pytest.fixture(scope="session")
def generate_clipMetadataRemove_params():
    """
    this fixture generates clipMetadataRemove params used by ad skip api requests

    """

    return{"type":"clipMetadataRemove"}

def generate_collectionStore_params():
    """
    This function generates collectionStore params.
    """

    return{"type":"collectionStore"}

def generate_contentStore_params():
    """
    This function generates contentStore params.
    """

    return{"type":"contentStore"}

def generate_collectionRemove_params():
    """
    This function generates collectionRemove params.
    """

    return{"type" : "collectionRemove"}

def generate_contentRemove_params():
    """
    This function generates contentRemove params.
    """

    return{"type" : "contentRemove"}


"""
PAYLOAD SECTION

"""
def payload_collectionStore():
    collectionStore={
	    "description" : "CableCo QE Test Ad Skip",
	    "partnerId" : "tivo:pt.3689",
	    "title" : "CableCo QE Test Ad Skip",
	    "type" : "collectionStore"
        }

    return json.dumps(collectionStore)

def payload_contentStore(collectionId):
    contentStore={
        "collectionId" : collectionId,
        "contentType" : "video",
        "isEpisode" : True,
        "movieYear" : "2015",
        "partnerId" : "tivo:pt.3689",
        "type" : "contentStore"
        }
    return json.dumps(contentStore)

def payload_contentRemove(contentId):
    contentRemove={
        "contentId" : contentId,
        "type" : "contentRemove"
        }
    return json.dumps(contentRemove)

def payload_collectionRemove(collectionId):
    collectionRemove={
        "collectionId" : collectionId,
        "type" : "collectionRemove"
        }
    return json.dumps(collectionRemove)

"""

Setup/Teardown
"""
@pytest.fixture(scope='session')
def setup_content(generate_middleMind_url, generate_appserver_url, generate_default_headers):

    response=requests.post(generate_middleMind_url, headers=generate_default_headers, params=generate_collectionStore_params(), data=payload_collectionStore())
    try:
        synthassert(response.status_code == 200, message = "collectionStore: Status code is not 200. Status code is " + str(response.status_code))
    except AssertionError as e:
        print(e)
        collectionId=None
        contentId = None
    else:
        try:
            json_data = response.json()
            collectionId= json_data["collectionId"]
            
        except (json.JSONDecodeError, KeyError):
            try:
                synthassert(False, message="collectionStore error", response=response)
            except AssertionError as e:
                print(e)
                collectionId = None
                contentId = None
        
    if collectionId != None:
        response=requests.post(generate_middleMind_url, headers=generate_default_headers, params=generate_contentStore_params(), data=payload_contentStore(collectionId))
        try:
            synthassert(response.status_code == 200, message = "contentStore: Status code is not 200. Status code is " + str(response.status_code))
        except AssertionError as e:
            print(e)
            contentId=None
        else:
            try:
                json_data = response.json()
                contentId = json_data["contentId"]
                
            except (json.JSONDecodeError, KeyError):
                try:
                    synthassert(False, message="contentStore error", response=response)
                except AssertionError as e:
                    print(e)
                    contentId = None

    yield contentId

# Yield has the same effect as return, but code following it is teardown code.

#   Teardown of content
    response=requests.post(generate_appserver_url, headers=generate_default_headers, params=generate_contentRemove_params(), data=payload_contentRemove(contentId))
   
#   Teardown of collection
    response=requests.post(generate_appserver_url, headers=generate_default_headers, params=generate_collectionRemove_params(), data=payload_collectionRemove(collectionId))



"""

EXPECTED RESULTS

"""

@pytest.fixture(scope="session")
def expected_clipMetadataStore(setup_content):
    contentId = setup_content
    clipMetadataStore={
            "authorBodyId": config['bodyId'],
            "authorId": "unknown",
            "clipMetadataId": config['clipMetadataId'],
            "contentId": contentId,
            "description": "clipMetadata_1A",
            "segmentType": "adSkip",
            "type": "clipMetadata"
        }

    return clipMetadataStore

@pytest.fixture(scope="session")
def expected_clipMetadataSearch(setup_content):
    contentId = setup_content
    clipMetadataSearch={
                    "authorBodyId": config['bodyId'],
                    "authorId": "unknown",
                    "clipMetadataId": config['clipMetadataId'],
                    "contentId": contentId,
                    "description": "clipMetadata_1A",
                    "isRevoked": False,
                    "segmentType": "adSkip",
                    "type": "clipMetadata"
                }
            

    return clipMetadataSearch