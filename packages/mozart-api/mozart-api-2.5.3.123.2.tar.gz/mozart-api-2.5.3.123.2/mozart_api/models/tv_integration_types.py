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


class TvIntegrationTypes(object):
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
    openapi_types = {"value": "str"}

    attribute_map = {"value": "value"}

    def __init__(
        self,
        value: Optional["TvIntegrationTypes.LTypeValue"] = None,
        local_vars_configuration=None,
    ):  # noqa: E501
        """TvIntegrationTypes - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._value = None
        self.discriminator = None

        if value is not None:
            self.value = value

    LTypeValue = Literal["ThirdParty", "Lge"]

    @property
    def value(self):
        # type: () -> 'TvIntegrationTypes.LTypeValue'
        """Gets the value of this TvIntegrationTypes.  # noqa: E501


        :return: The value of this TvIntegrationTypes.  # noqa: E501
        :rtype: 'TvIntegrationTypes.LTypeValue'
        """
        return self._value

    @value.setter
    def value(self, value):
        # type: ('TvIntegrationTypes.LTypeValue') -> None
        """Sets the value of this TvIntegrationTypes.


        :param value: The value of this TvIntegrationTypes.  # noqa: E501
        :type value: 'TvIntegrationTypes.LTypeValue'
        :rtype: None
        """
        allowed_values = ["ThirdParty", "Lge"]  # noqa: E501
        if (
            self.local_vars_configuration.client_side_validation
            and value not in allowed_values
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `value` ({0}), must be one of {1}".format(  # noqa: E501
                    value, allowed_values
                )
            )

        self._value = value

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
        if not isinstance(other, TvIntegrationTypes):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, TvIntegrationTypes):
            return True

        return self.to_dict() != other.to_dict()
