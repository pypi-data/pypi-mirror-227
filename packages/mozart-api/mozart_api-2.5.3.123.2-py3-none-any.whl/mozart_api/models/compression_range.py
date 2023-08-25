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

from mozart_api.models.compression import Compression

from mozart_api.configuration import Configuration


class CompressionRange(object):
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
    openapi_types = {"default": "Compression", "range": "list[Compression]"}

    attribute_map = {"default": "default", "range": "range"}

    def __init__(
        self,
        default: Optional[Compression] = None,
        range: Optional[List[Compression]] = None,
        local_vars_configuration=None,
    ):  # noqa: E501
        """CompressionRange - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._default = None
        self._range = None
        self.discriminator = None

        self.default = default
        self.range = range

    @property
    def default(self):
        # type: () -> Compression
        """Gets the default of this CompressionRange.  # noqa: E501


        :return: The default of this CompressionRange.  # noqa: E501
        :rtype: Compression
        """
        return self._default

    @default.setter
    def default(self, default):
        # type: (Compression) -> None
        """Sets the default of this CompressionRange.


        :param default: The default of this CompressionRange.  # noqa: E501
        :type default: Compression
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
        # type: () -> List[Compression]
        """Gets the range of this CompressionRange.  # noqa: E501

        compression range  # noqa: E501

        :return: The range of this CompressionRange.  # noqa: E501
        :rtype: List[Compression]
        """
        return self._range

    @range.setter
    def range(self, range):
        # type: (list[Compression]) -> None
        """Sets the range of this CompressionRange.

        compression range  # noqa: E501

        :param range: The range of this CompressionRange.  # noqa: E501
        :type range: list[Compression]
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
        if not isinstance(other, CompressionRange):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CompressionRange):
            return True

        return self.to_dict() != other.to_dict()
