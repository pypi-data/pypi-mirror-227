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

from mozart_api.models.tv_integration_types import TvIntegrationTypes

from mozart_api.configuration import Configuration


class TvInfoEventData(object):
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
    openapi_types = {"integration": "TvIntegrationTypes"}

    attribute_map = {"integration": "integration"}

    def __init__(
        self,
        integration: Optional[TvIntegrationTypes] = None,
        local_vars_configuration=None,
    ):  # noqa: E501
        """TvInfoEventData - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._integration = None
        self.discriminator = None

        if integration is not None:
            self.integration = integration

    @property
    def integration(self):
        # type: () -> TvIntegrationTypes
        """Gets the integration of this TvInfoEventData.  # noqa: E501


        :return: The integration of this TvInfoEventData.  # noqa: E501
        :rtype: TvIntegrationTypes
        """
        return self._integration

    @integration.setter
    def integration(self, integration):
        # type: (TvIntegrationTypes) -> None
        """Sets the integration of this TvInfoEventData.


        :param integration: The integration of this TvInfoEventData.  # noqa: E501
        :type integration: TvIntegrationTypes
        :rtype: None
        """

        self._integration = integration

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
        if not isinstance(other, TvInfoEventData):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, TvInfoEventData):
            return True

        return self.to_dict() != other.to_dict()
