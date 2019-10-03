import pytest
import json
from pytest_lib import config

class adSkipPayloads(object):
    def payload_clipMetadataStore(self, contentId):
        clipMetadataStore = {
            "authorBodyId" : config["bodyId"],
            "authorId" : "unknown",
            "clipMetadataId" : config["clipMetadataId"],
            "contentId" : contentId,
            "description" : "clipMetadata_1A",
            "isRevoked" : False,
            "segment" : [
                {
                    "endOffset" : "1197312",
                    "startOffset" : "1075891",
                    "type" : "clipSegment"
                }
            ],
            "segmentType" : "adSkip",
            "syncMark" : [
                {
                    "hash" : "4090466097",
                    "timestamp" : "1059508",
                    "type" : "clipSyncMark"
                },
                {
                    "hash" : "2907989715",
                    "timestamp" : "1062745",
                    "type" : "clipSyncMark"
                },
                {
                    "hash" : "4103061638",
                    "timestamp" : "1063579",
                    "type" : "clipSyncMark"
                },
                {
                    "hash" : "773751968",
                    "timestamp" : "1065814",
                    "type" : "clipSyncMark"
                },
                {
                    "hash" : "4028542047",
                    "timestamp" : "1067883",
                    "type" : "clipSyncMark"
                },
                {
                    "hash" : "3682783438",
                    "timestamp" : "1069218",
                    "type" : "clipSyncMark"
                },
                {
                    "hash" : "2637931466",
                    "timestamp" : "1069919",
                    "type" : "clipSyncMark"
                },
                {
                    "hash" : "4212699772",
                    "timestamp" : "1071387",
                    "type" : "clipSyncMark"
                },
                {
                    "hash" : "3308649630",
                    "timestamp" : "1074123",
                    "type" : "clipSyncMark"
                },
                {
                    "hash" : "1238565687",
                    "timestamp" : "1075791",
                    "type" : "clipSyncMark"
                },
                {
                    "hash" : "50582259",
                    "timestamp" : "1075925",
                    "type" : "clipSyncMark"
                },
                {
                    "hash" : "2561205050",
                    "timestamp" : "1078294",
                    "type" : "clipSyncMark"
                },
                {
                    "hash" : "2424339896",
                    "timestamp" : "1078761",
                    "type" : "clipSyncMark"
                },
                {
                    "hash" : "3746896772",
                    "timestamp" : "1079428",
                    "type" : "clipSyncMark"
                },
                {
                    "hash" : "514038492",
                    "timestamp" : "1081330",
                    "type" : "clipSyncMark"
                },
                {
                    "hash" : "502429023",
                    "timestamp" : "1083699",
                    "type" : "clipSyncMark"
                },
                {
                    "hash" : "2586500571",
                    "timestamp" : "1084800",
                    "type" : "clipSyncMark"
                },
                {
                    "hash" : "2245260266",
                    "timestamp" : "1086201",
                    "type" : "clipSyncMark"
                },
                {
                    "hash" : "1318565206",
                    "timestamp" : "1092942",
                    "type" : "clipSyncMark"
                },
                {
                    "hash" : "3608548650",
                    "timestamp" : "1093809",
                    "type" : "clipSyncMark"
                },
                {
                    "hash" : "1881875665",
                    "timestamp" : "1095277",
                    "type" : "clipSyncMark"
                },
                {
                    "hash" : "131987701",
                    "timestamp" : "1098113",
                    "type" : "clipSyncMark"
                },
                {
                    "hash" : "1135836371",
                    "timestamp" : "1100249",
                    "type" : "clipSyncMark"
                },
                {
                    "hash" : "2652642041",
                    "timestamp" : "1103552",
                    "type" : "clipSyncMark"
                },
                {
                    "hash" : "709736615",
                    "timestamp" : "1106355",
                    "type" : "clipSyncMark"
                },
                {
                    "hash" : "501441023",
                    "timestamp" : "1109058",
                    "type" : "clipSyncMark"
                },
                {
                    "hash" : "1769810840",
                    "timestamp" : "1111160",
                    "type" : "clipSyncMark"
                },
                {
                    "hash" : "3965082580",
                    "timestamp" : "1112027",
                    "type" : "clipSyncMark"
                }
            ],
            "type" : "clipMetadataStore"
        }

        return json.dumps(clipMetadataStore)

    def payload_clipMetadataSearch(self, contentId):
        clipMetadataSearch = {
            "contentId" : contentId,
            "segmentType" : "adSkip",
            "levelOfDetail" : "high",
            "type" : "clipMetadataSearch"
        }

        return json.dumps(clipMetadataSearch)
    
    def payload_clipMetadataStateGet(self, contentId):
        clipMetadataStateGet = {
            "contentId" : contentId,
            "type" : "clipMetadataStateGet"
        }

        return json.dumps(clipMetadataStateGet)

    def payload_clipMetadataRemove(self):
        clipMetadataRemove = {
            "clipMetadataId" : config["clipMetadataId"],
            "type" : "clipMetadataRemove"
        }

        return json.dumps(clipMetadataRemove)