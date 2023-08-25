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

import mozart_api
from mozart_api.api.product_api import ProductApi  # noqa: E501
from mozart_api.rest import ApiException


class TestProductApi(unittest.TestCase):
    """ProductApi unit test stubs"""

    def setUp(self):
        self.api = mozart_api.api.product_api.ProductApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_get_product_state(self):
        """Test case for get_product_state

        Get the overall state from the product  # noqa: E501
        """
        pass

    def test_set_product_friendly_name(self):
        """Test case for set_product_friendly_name

        Set the friendly name  # noqa: E501
        """
        pass


if __name__ == "__main__":
    unittest.main()
