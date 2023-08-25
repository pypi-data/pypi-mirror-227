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

from mozart_api.models.playback_content_metadata import PlaybackContentMetadata

from mozart_api.configuration import Configuration


class PlaybackError(object):
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
    openapi_types = {"error": "str", "item": "PlaybackContentMetadata"}

    attribute_map = {"error": "error", "item": "item"}

    def __init__(
        self,
        error: Optional[str] = None,
        item: Optional[PlaybackContentMetadata] = None,
        local_vars_configuration=None,
    ):  # noqa: E501
        """PlaybackError - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._error = None
        self._item = None
        self.discriminator = None

        if error is not None:
            self.error = error
        if item is not None:
            self.item = item

    @property
    def error(self):
        # type: () -> str
        """Gets the error of this PlaybackError.  # noqa: E501


        :return: The error of this PlaybackError.  # noqa: E501
        :rtype: str
        """
        return self._error

    @error.setter
    def error(self, error):
        # type: (str) -> None
        """Sets the error of this PlaybackError.


        :param error: The error of this PlaybackError.  # noqa: E501
        :type error: str
        :rtype: None
        """

        self._error = error

    @property
    def item(self):
        # type: () -> PlaybackContentMetadata
        """Gets the item of this PlaybackError.  # noqa: E501


        :return: The item of this PlaybackError.  # noqa: E501
        :rtype: PlaybackContentMetadata
        """
        return self._item

    @item.setter
    def item(self, item):
        # type: (PlaybackContentMetadata) -> None
        """Sets the item of this PlaybackError.


        :param item: The item of this PlaybackError.  # noqa: E501
        :type item: PlaybackContentMetadata
        :rtype: None
        """

        self._item = item

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
        if not isinstance(other, PlaybackError):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, PlaybackError):
            return True

        return self.to_dict() != other.to_dict()
