# coding: utf-8

"""
    Mozart platform API

    API for interacting with the Mozart platform.  # noqa: E501

    The version of the OpenAPI document: 0.2.0
    Contact: support@bang-olufsen.dk
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import mozart_api
from mozart_api.models.scene_trigger_base_properties import (
    SceneTriggerBaseProperties,
)  # noqa: E501
from mozart_api.rest import ApiException


class TestSceneTriggerBaseProperties(unittest.TestCase):
    """SceneTriggerBaseProperties unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test SceneTriggerBaseProperties
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # model = mozart_api.models.scene_trigger_base_properties.SceneTriggerBaseProperties()  # noqa: E501
        if include_optional:
            return SceneTriggerBaseProperties(
                action_list=[
                    {"type": "volume", "volumeLevel": 35},
                    {"radioStationId": "8779112938791514", "type": "radio"},
                    {"stopDuration": 1300, "type": "stop"},
                ],
                scene_list=["0"],
            )
        else:
            return SceneTriggerBaseProperties()

    def testSceneTriggerBaseProperties(self):
        """Test SceneTriggerBaseProperties"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()
