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


class ProductCurtainStatus(object):
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
    openapi_types = {"moving": "bool", "position": "str"}

    attribute_map = {"moving": "moving", "position": "position"}

    def __init__(
        self,
        moving: Optional[bool] = None,
        position: Optional["ProductCurtainStatus.LTypePosition"] = None,
        local_vars_configuration=None,
    ):  # noqa: E501
        """ProductCurtainStatus - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._moving = None
        self._position = None
        self.discriminator = None

        if moving is not None:
            self.moving = moving
        if position is not None:
            self.position = position

    @property
    def moving(self):
        # type: () -> bool
        """Gets the moving of this ProductCurtainStatus.  # noqa: E501


        :return: The moving of this ProductCurtainStatus.  # noqa: E501
        :rtype: bool
        """
        return self._moving

    @moving.setter
    def moving(self, moving):
        # type: (bool) -> None
        """Sets the moving of this ProductCurtainStatus.


        :param moving: The moving of this ProductCurtainStatus.  # noqa: E501
        :type moving: bool
        :rtype: None
        """

        self._moving = moving

    LTypePosition = Literal["unknown", "closed", "narrow", "wide"]

    @property
    def position(self):
        # type: () -> 'ProductCurtainStatus.LTypePosition'
        """Gets the position of this ProductCurtainStatus.  # noqa: E501


        :return: The position of this ProductCurtainStatus.  # noqa: E501
        :rtype: 'ProductCurtainStatus.LTypePosition'
        """
        return self._position

    @position.setter
    def position(self, position):
        # type: ('ProductCurtainStatus.LTypePosition') -> None
        """Sets the position of this ProductCurtainStatus.


        :param position: The position of this ProductCurtainStatus.  # noqa: E501
        :type position: 'ProductCurtainStatus.LTypePosition'
        :rtype: None
        """
        allowed_values = ["unknown", "closed", "narrow", "wide"]  # noqa: E501
        if (
            self.local_vars_configuration.client_side_validation
            and position not in allowed_values
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `position` ({0}), must be one of {1}".format(  # noqa: E501
                    position, allowed_values
                )
            )

        self._position = position

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
        if not isinstance(other, ProductCurtainStatus):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ProductCurtainStatus):
            return True

        return self.to_dict() != other.to_dict()
