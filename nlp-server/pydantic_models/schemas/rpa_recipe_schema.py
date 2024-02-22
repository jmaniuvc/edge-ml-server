"""
This is a module that does Machine Learning Schema.
"""

__author__ = "jmaniuvc@uvc.co.kr"
__copyright__ = "Copyright 2023, NT Team"

from pydantic import BaseModel


class RPARecipeBody(BaseModel):
    """ Structure that appears when requesting preprocessing API """
    recipeName: str
    msg: str


class RPARecipeRequestBody(BaseModel):
    """ Structure that appears when requesting preprocessing API """
    data: RPARecipeBody
