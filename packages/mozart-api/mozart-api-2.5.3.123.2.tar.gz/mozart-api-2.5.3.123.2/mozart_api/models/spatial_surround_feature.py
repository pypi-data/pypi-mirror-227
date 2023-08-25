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

from mozart_api.models.spatial_surround import SpatialSurround

from mozart_api.configuration import Configuration


class SpatialSurroundFeature(object):
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
        "default": "SpatialSurround",
        "range": "list[SpatialSurround]",
    }

    attribute_map = {"value": "value", "default": "default", "range": "range"}

    def __init__(
        self,
        value: Optional[float] = None,
        default: Optional[SpatialSurround] = None,
        range: Optional[List[SpatialSurround]] = None,
        local_vars_configuration=None,
    ):  # noqa: E501
        """SpatialSurroundFeature - a model defined in OpenAPI"""  # noqa: E501
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
        """Gets the value of this SpatialSurroundFeature.  # noqa: E501

        Selected spatial-surround value  # noqa: E501

        :return: The value of this SpatialSurroundFeature.  # noqa: E501
        :rtype: float
        """
        return self._value

    @value.setter
    def value(self, value):
        # type: (float) -> None
        """Sets the value of this SpatialSurroundFeature.

        Selected spatial-surround value  # noqa: E501

        :param value: The value of this SpatialSurroundFeature.  # noqa: E501
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
        # type: () -> SpatialSurround
        """Gets the default of this SpatialSurroundFeature.  # noqa: E501


        :return: The default of this SpatialSurroundFeature.  # noqa: E501
        :rtype: SpatialSurround
        """
        return self._default

    @default.setter
    def default(self, default):
        # type: (SpatialSurround) -> None
        """Sets the default of this SpatialSurroundFeature.


        :param default: The default of this SpatialSurroundFeature.  # noqa: E501
        :type default: SpatialSurround
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
        # type: () -> List[SpatialSurround]
        """Gets the range of this SpatialSurroundFeature.  # noqa: E501

        spatial-surround range  # noqa: E501

        :return: The range of this SpatialSurroundFeature.  # noqa: E501
        :rtype: List[SpatialSurround]
        """
        return self._range

    @range.setter
    def range(self, range):
        # type: (list[SpatialSurround]) -> None
        """Sets the range of this SpatialSurroundFeature.

        spatial-surround range  # noqa: E501

        :param range: The range of this SpatialSurroundFeature.  # noqa: E501
        :type range: list[SpatialSurround]
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
        if not isinstance(other, SpatialSurroundFeature):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, SpatialSurroundFeature):
            return True

        return self.to_dict() != other.to_dict()
