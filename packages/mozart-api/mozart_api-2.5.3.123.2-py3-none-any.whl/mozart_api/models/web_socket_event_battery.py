# coding: utf-8

"""
    Mozart platform API

    API for interacting with the Mozart platform.  # noqa: E501

    The version of the OpenAPI document: 0.2.0
    Contact: support@bang-olufsen.dk
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from datetime import datetime
from typing import List, Dict, Literal, Optional

from mozart_api.models.battery_state import BatteryState

from mozart_api.configuration import Configuration


class WebSocketEventBattery(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {"event_data": "BatteryState", "event_type": "str"}

    attribute_map = {"event_data": "eventData", "event_type": "eventType"}

    def __init__(
        self,
        event_data: Optional[BatteryState] = None,
        event_type: Optional[str] = None,
        local_vars_configuration=None,
    ):  # noqa: E501
        """WebSocketEventBattery - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._event_data = None
        self._event_type = None
        self.discriminator = None

        if event_data is not None:
            self.event_data = event_data
        if event_type is not None:
            self.event_type = event_type

    @property
    def event_data(self):
        # type: () -> BatteryState
        """Gets the event_data of this WebSocketEventBattery.  # noqa: E501


        :return: The event_data of this WebSocketEventBattery.  # noqa: E501
        :rtype: BatteryState
        """
        return self._event_data

    @event_data.setter
    def event_data(self, event_data):
        # type: (BatteryState) -> None
        """Sets the event_data of this WebSocketEventBattery.


        :param event_data: The event_data of this WebSocketEventBattery.  # noqa: E501
        :type event_data: BatteryState
        :rtype: None
        """

        self._event_data = event_data

    @property
    def event_type(self):
        # type: () -> str
        """Gets the event_type of this WebSocketEventBattery.  # noqa: E501


        :return: The event_type of this WebSocketEventBattery.  # noqa: E501
        :rtype: str
        """
        return self._event_type

    @event_type.setter
    def event_type(self, event_type):
        # type: (str) -> None
        """Sets the event_type of this WebSocketEventBattery.


        :param event_type: The event_type of this WebSocketEventBattery.  # noqa: E501
        :type event_type: str
        :rtype: None
        """

        self._event_type = event_type

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(
                    map(lambda x: x.to_dict() if hasattr(x, "to_dict") else x, value)
                )
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(
                    map(
                        lambda item: (item[0], item[1].to_dict())
                        if hasattr(item[1], "to_dict")
                        else item,
                        value.items(),
                    )
                )
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, WebSocketEventBattery):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, WebSocketEventBattery):
            return True

        return self.to_dict() != other.to_dict()
