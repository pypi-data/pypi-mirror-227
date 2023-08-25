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
from mozart_api.models.remote_menu_item import RemoteMenuItem  # noqa: E501
from mozart_api.rest import ApiException


class TestRemoteMenuItem(unittest.TestCase):
    """RemoteMenuItem unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test RemoteMenuItem
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # model = mozart_api.models.remote_menu_item.RemoteMenuItem()  # noqa: E501
        if include_optional:
            return RemoteMenuItem(
                action_list=[
                    {"type": "volume", "volumeLevel": 35},
                    {"radioStationId": "8779112938791514", "type": "radio"},
                    {"stopDuration": 1300, "type": "stop"},
                ],
                scene_list=["0"],
                disabled=True,
                dynamic_list="none",
                first_child_menu_item_id="0",
                label="0",
                next_sibling_menu_item_id="0",
                parent_menu_item_id="0",
                available=True,
                content={"contentUri": "tv://netflix", "label": "Netflix"},
                fixed=True,
                id="0",
            )
        else:
            return RemoteMenuItem(
                fixed=True,
                id="0",
            )

    def testRemoteMenuItem(self):
        """Test RemoteMenuItem"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()
