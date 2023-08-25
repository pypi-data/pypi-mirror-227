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
from mozart_api.models.beolink_experience import BeolinkExperience  # noqa: E501
from mozart_api.rest import ApiException


class TestBeolinkExperience(unittest.TestCase):
    """BeolinkExperience unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test BeolinkExperience
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # model = mozart_api.models.beolink_experience.BeolinkExperience()  # noqa: E501
        if include_optional:
            return BeolinkExperience(
                category="TV",
                id="0",
                linkable=True,
                name="0",
                product_friendly_name="0",
                source_friendly_name="0",
                type="0",
                unique_source_id="0",
            )
        else:
            return BeolinkExperience(
                category="TV",
                id="0",
                linkable=True,
                name="0",
                type="0",
                unique_source_id="0",
            )

    def testBeolinkExperience(self):
        """Test BeolinkExperience"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()
