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

from mozart_api.models.tone_touch_type import ToneTouchType

from mozart_api.configuration import Configuration


class ToneTouchYFeature(object):
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
        "value": "float",
        "default": "ToneTouchType",
        "range": "list[ToneTouchType]",
    }

    attribute_map = {"value": "value", "default": "default", "range": "range"}

    def __init__(
        self,
        value: Optional[float] = None,
        default: Optional[ToneTouchType] = None,
        range: Optional[List[ToneTouchType]] = None,
        local_vars_configuration=None,
    ):  # noqa: E501
        """ToneTouchYFeature - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._value = None
        self._default = None
        self._range = None
        self.discriminator = None

        self.value = value
        self.default = default
        self.range = range

    @property
    def value(self):
        # type: () -> float
        """Gets the value of this ToneTouchYFeature.  # noqa: E501


        :return: The value of this ToneTouchYFeature.  # noqa: E501
        :rtype: float
        """
        return self._value

    @value.setter
    def value(self, value):
        # type: (float) -> None
        """Sets the value of this ToneTouchYFeature.


        :param value: The value of this ToneTouchYFeature.  # noqa: E501
        :type value: float
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
        # type: () -> ToneTouchType
        """Gets the default of this ToneTouchYFeature.  # noqa: E501


        :return: The default of this ToneTouchYFeature.  # noqa: E501
        :rtype: ToneTouchType
        """
        return self._default

    @default.setter
    def default(self, default):
        # type: (ToneTouchType) -> None
        """Sets the default of this ToneTouchYFeature.


        :param default: The default of this ToneTouchYFeature.  # noqa: E501
        :type default: ToneTouchType
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
    def range(self):
        # type: () -> List[ToneTouchType]
        """Gets the range of this ToneTouchYFeature.  # noqa: E501

        Product and role specific tone touch X or Y range  # noqa: E501

        :return: The range of this ToneTouchYFeature.  # noqa: E501
        :rtype: List[ToneTouchType]
        """
        return self._range

    @range.setter
    def range(self, range):
        # type: (list[ToneTouchType]) -> None
        """Sets the range of this ToneTouchYFeature.

        Product and role specific tone touch X or Y range  # noqa: E501

        :param range: The range of this ToneTouchYFeature.  # noqa: E501
        :type range: list[ToneTouchType]
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
        if not isinstance(other, ToneTouchYFeature):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ToneTouchYFeature):
            return True

        return self.to_dict() != other.to_dict()
