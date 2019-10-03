"""
Function to compare two JSON structures for matching values. It ignores any key in json_result that is
not in json_expected.

"""


def check_ignore_missing(json_result, json_expected):
        for item in json_result:
                if item in json_expected:
                        if json_result[item] != json_expected[item]:
                                return False
        return True