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
from mozart_api.models.bluetooth_device_list import BluetoothDeviceList  # noqa: E501
from mozart_api.rest import ApiException


class TestBluetoothDeviceList(unittest.TestCase):
    """BluetoothDeviceList unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test BluetoothDeviceList
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # model = mozart_api.models.bluetooth_device_list.BluetoothDeviceList()  # noqa: E501
        if include_optional:
            return BluetoothDeviceList(
                items=[
                    mozart_api.models.bluetooth_device.BluetoothDevice(
                        address="0",
                        connected=True,
                        name="0",
                    )
                ]
            )
        else:
            return BluetoothDeviceList()

    def testBluetoothDeviceList(self):
        """Test BluetoothDeviceList"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()
