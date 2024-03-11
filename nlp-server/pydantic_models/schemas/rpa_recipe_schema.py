"""
This is a module that does Machine Learning Schema.
"""

__author__ = "jmaniuvc@uvc.co.kr"
__copyright__ = "Copyright 2024, NT Team"


from enum import Enum
from typing import List, Union, Optional, Any
from pydantic import BaseModel, field_validator, validator, ValidationInfo


class RecipeOperator(str, Enum):
    """ Structure that appears when requesting preprocessing API """
    EQ = 'EQ'
    NEQ = 'NEQ'
    LT = 'LT'
    GT = 'GT'


class RecipeRelationship(str, Enum):
    """ Structure that appears when requesting preprocessing API """
    AND = 'AND'
    OR = 'OR'
    
    

class RecipeActionType(str, Enum):
    """ Structure that appears when requesting preprocessing API """
    alarm = 'alarm'
    control = 'control'


class TagIDNameAndNamesBody(BaseModel):
    """ Structure that appears when requesting preprocessing API """
    tagId: str
    tagName: str


class RPARecipeRequestBody(BaseModel):
    """ Structure that appears when requesting preprocessing API """
    msg: str
    tagIdsAndNames: List[TagIDNameAndNamesBody]


class RPARecipeConditions(BaseModel):
    """ Structure that appears when requesting preprocessing API """
    tagId: str
    operator: Union[RecipeOperator, None]
    value: Union[str, int, float]
    andOrRelationship: Union[RecipeRelationship, None]
    conditionGroupId: Union[int, None]

    @field_validator('andOrRelationship', mode='before')
    def check_relationship_type(v, _):
        if v not in RecipeRelationship.__members__.keys():
            return None
        return v

    @field_validator('operator', mode='before')
    def check_operator_type(v, _):
        if v not in RecipeOperator.__members__.keys():
            return None
        return v

    @field_validator('conditionGroupId', mode='before')
    def check_int_type(v, _):
        if not isinstance(v, int):
            return None
        return v


class RPARecipeActions(BaseModel):
    """ Structure that appears when requesting preprocessing API """
    actionType: Union[RecipeActionType, None]
    tagId: Union[str, None]
    operator: Union[str, None]
    value: Union[float, None]
    emailRecipient: Union[str, None]
    emailContents: Union[str, None]

    @field_validator('actionType', mode='before')
    def check_action_type(v, _):
        if v not in RecipeActionType.__members__.keys():
            return None
        return v

    @field_validator('operator', mode='before')
    def check_operator_type(v, _):
        if v not in RecipeOperator.__members__.keys():
            return None
        return v

    @field_validator('tagId', 'emailRecipient', 'emailContents', mode='before')
    def check_str_type(v, _):
        if not isinstance(v, str):
            return None
        return v

    @field_validator('value', mode='before')
    def check_float_type(v, _):
        if not isinstance(v, float):
            return None
        return v


class RPARecipeResponseBody(BaseModel):
    """ Structure that appears when requesting preprocessing API """
    conditions: List[RPARecipeConditions]
    actions: List[RPARecipeActions]
