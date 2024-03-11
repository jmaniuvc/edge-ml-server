# !/usr/bin/env python3
"""
This is a module that does data NLP Server.
"""

__author__ = "jmaniuvc@uvc.co.kr"
__copyright__ = "Copyright 2024, AI Team"


import json


class ValidationRecipe():
    """ Validation Recipe """
    def __init__(self, draft) -> None:
        self.draft = json.loads(draft)
        self.validate_conditions(self.draft['conditions'])
        self.validate_actions(self.draft['actions'])

    def validate_actions(self, actions) -> None:
        """ validate Actions """
        # TODO
        for action in actions:
            if action['actionType'] == 'control':
                action['operator'] = 'EQ'
                action['emailRecipient'] = None
                action['emailContents'] = None
            elif action['actionType'] == 'alarm':
                action['tagId'] = None
                action['operator'] = None
                action['value'] = None
            else:
                pass
        self.actions = actions

    def validate_conditions(self, conditions):
        """ Validate Conditions """
        self.conditions = conditions

    def get_recipe(self):
        """ Get Recipe """
        recipe = {'conditions': self.conditions,
                  'actions': self.actions}
        return recipe
