"""
This is a module that does Machine Learning Schema.
"""

__author__ = "jmaniuvc@uvc.co.kr"
__copyright__ = "Copyright 2023, NT Team"

from typing import List, Any
from pydantic import BaseModel


class RealTimeRequestBody(BaseModel):
    """ Structure that appears when requesting preprocessing API """
    DEVICE_ID: str
    TAGS: List[Any]
    DATE_TIME: str
