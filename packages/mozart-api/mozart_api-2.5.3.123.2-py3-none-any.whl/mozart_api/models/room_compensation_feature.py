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


from mozart_api.configuration import Configuration


class RoomCompensationFeature(object):
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
    openapi_types = {
        "value": "list[str]",
        "default": "list[str]",
        "max_items": "int",
        "range": "list[str]",
    }

    attribute_map = {
        "value": "value",
        "default": "default",
        "max_items": "maxItems",
        "range": "range",
    }

    def __init__(
        self,
        value: Optional[List[str]] = None,
        default: Optional[List[str]] = None,
        max_items: Optional[int] = None,
        range: Optional[List[str]] = None,
        local_vars_configuration=None,
    ):  # noqa: E501
        """RoomCompensationFeature - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._value = None
        self._default = None
        self._max_items = None
        self._range = None
        self.discriminator = None

        self.value = value
        self.default = default
        if max_items is not None:
            self.max_items = max_items
        self.range = range

    @property
    def value(self):
        # type: () -> List[str]
        """Gets the value of this RoomCompensationFeature.  # noqa: E501

        List of room compensation sweeps to combine. No room compensation is done if this list is empty. The maximum length of this list is product specific.   # noqa: E501

        :return: The value of this RoomCompensationFeature.  # noqa: E501
        :rtype: List[str]
        """
        return self._value

    @value.setter
    def value(self, value):
        # type: (list[str]) -> None
        """Sets the value of this RoomCompensationFeature.

        List of room compensation sweeps to combine. No room compensation is done if this list is empty. The maximum length of this list is product specific.   # noqa: E501

        :param value: The value of this RoomCompensationFeature.  # noqa: E501
        :type value: list[str]
        :rtype: None
        """
        if (
            self.local_vars_configuration.client_side_validation and value is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `value`, must not be `None`"
            )  # noqa: E501

        self._value = value

    @property
    def default(self):
        # type: () -> List[str]
        """Gets the default of this RoomCompensationFeature.  # noqa: E501

        List of room compensation sweeps to combine. No room compensation is done if this list is empty. The maximum length of this list is product specific.   # noqa: E501

        :return: The default of this RoomCompensationFeature.  # noqa: E501
        :rtype: List[str]
        """
        return self._default

    @default.setter
    def default(self, default):
        # type: (list[str]) -> None
        """Sets the default of this RoomCompensationFeature.

        List of room compensation sweeps to combine. No room compensation is done if this list is empty. The maximum length of this list is product specific.   # noqa: E501

        :param default: The default of this RoomCompensationFeature.  # noqa: E501
        :type default: list[str]
        :rtype: None
        """
        if (
            self.local_vars_configuration.client_side_validation and default is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `default`, must not be `None`"
            )  # noqa: E501

        self._default = default

    @property
    def max_items(self):
        # type: () -> int
        """Gets the max_items of this RoomCompensationFeature.  # noqa: E501

        Maximum number of items in the `value` field  # noqa: E501

        :return: The max_items of this RoomCompensationFeature.  # noqa: E501
        :rtype: int
        """
        return self._max_items

    @max_items.setter
    def max_items(self, max_items):
        # type: (int) -> None
        """Sets the max_items of this RoomCompensationFeature.

        Maximum number of items in the `value` field  # noqa: E501

        :param max_items: The max_items of this RoomCompensationFeature.  # noqa: E501
        :type max_items: int
        :rtype: None
        """
        if (
            self.local_vars_configuration.client_side_validation
            and max_items is not None
            and max_items > 20
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `max_items`, must be a value less than or equal to `20`"
            )  # noqa: E501
        if (
            self.local_vars_configuration.client_side_validation
            and max_items is not None
            and max_items < 1
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `max_items`, must be a value greater than or equal to `1`"
            )  # noqa: E501

        self._max_items = max_items

    @property
    def range(self):
        # type: () -> List[str]
        """Gets the range of this RoomCompensationFeature.  # noqa: E501

        Possible values for the `value` field  # noqa: E501

        :return: The range of this RoomCompensationFeature.  # noqa: E501
        :rtype: List[str]
        """
        return self._range

    @range.setter
    def range(self, range):
        # type: (list[str]) -> None
        """Sets the range of this RoomCompensationFeature.

        Possible values for the `value` field  # noqa: E501

        :param range: The range of this RoomCompensationFeature.  # noqa: E501
        :type range: list[str]
        :rtype: None
        """
        if (
            self.local_vars_configuration.client_side_validation and range is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `range`, must not be `None`"
            )  # noqa: E501

        self._range = range

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
        if not isinstance(other, RoomCompensationFeature):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, RoomCompensationFeature):
            return True

        return self.to_dict() != other.to_dict()
