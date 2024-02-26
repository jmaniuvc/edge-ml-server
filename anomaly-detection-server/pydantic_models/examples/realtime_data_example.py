#!/usr/bin/env python3

"""
This is a module that does preprocessing API request example.
"""

__author__ = "jmaniuvc@uvc.co.kr"
__copyright__ = "Copyright 2023, NT Team"

realtime_data_exam = {
    "SmartConnector": {
        "summary": "Smart Connector example",
        "description": "A **Smart Connector** item works correctly.",
        "value": {
            "body": {
                "DEVICE_ID": "DEV_MODBUS_01",
                "TAGS": [
                    {"TAG_ID": "TAG_01", "TAG_VALUE": "0", "IS_ERROR": "N", "NODE_ID": "A123"},
                    {"TAG_ID": "TAG_02", "TAG_VALUE": "0", "IS_ERROR": "N", "NODE_ID": "B123"},
                    {"TAG_ID": "TAG_03", "TAG_VALUE": "0", "IS_ERROR": "N", "NODE_ID": "C123"},
                    {"TAG_ID": "TAG_04", "TAG_VALUE": "0", "IS_ERROR": "N", "NODE_ID": "D123"},
                    {"TAG_ID": "TAG_05", "TAG_VALUE": "0", "IS_ERROR": "N", "NODE_ID": "E123"},
                    {"TAG_ID": "TAG_06", "TAG_VALUE": "0", "IS_ERROR": "N", "NODE_ID": "F123"},
                    {"TAG_ID": "TAG_07", "TAG_VALUE": "0", "IS_ERROR": "N", "NODE_ID": "G123"},
                    {"TAG_ID": "TAG_08", "TAG_VALUE": "0", "IS_ERROR": "N", "NODE_ID": "H123"}
                ],
                "DATE_TIME": "2024-01-29T17:07:13.6144902+09:00",
            }
        }
    }
}
