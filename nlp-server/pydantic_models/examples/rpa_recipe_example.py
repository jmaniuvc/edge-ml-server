#!/usr/bin/env python3

"""
This is a module that does preprocessing API request example.
"""

__author__ = "jmaniuvc@uvc.co.kr"
__copyright__ = "Copyright 2023, NT Team"

rpa_recipe_exam = {
    "Frontech1": {
        "summary": "Frontech example1",
        # "description": "A **Frontech** item works correctly.",
        "value": {
            "msg": "에어 누출이 없고 에어압력 지침이 4~6Mpa라면 에어 레귤레이터를 점검/수리/교체하는 레시피 만들어줘.",
            "tagIdsAndNames": [
                {"tagId": "TAGID1", "tagName": "에어누출"},
                {"tagId": "TAGID2", "tagName": "에어압력"},
                {"tagId": "TAGID3", "tagName": "레귤레이터"}
            ]
        }
    },
    "Frontech2": {
        "summary": "Frontech example2",
        # "description": "A **Frontech** item works correctly.",
        "value": {
            "msg": "윤활부가 10이상 20이하고 세퍼레이터와 냉각부가 5이하면 알림을 발생시켜라.",
            "tagIdsAndNames": [
                {"tagId": "TAGID1", "tagName": "윤활부"},
                {"tagId": "TAGID2", "tagName": "세퍼레이터"},
                {"tagId": "TAGID3", "tagName": "냉각부"}
            ]
        }
    }
}
