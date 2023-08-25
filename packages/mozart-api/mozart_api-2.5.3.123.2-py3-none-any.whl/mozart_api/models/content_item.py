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

from mozart_api.models.source_type_enum import SourceTypeEnum

from mozart_api.configuration import Configuration


class ContentItem(object):
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
        "categories": "list[str]",
        "content_uri": "str",
        "label": "str",
        "source": "SourceTypeEnum",
    }

    attribute_map = {
        "categories": "categories",
        "content_uri": "contentUri",
        "label": "label",
        "source": "source",
    }

    def __init__(
        self,
        categories: Optional["ContentItem.LTypeCategories"] = None,
        content_uri: Optional[str] = None,
        label: Optional[str] = None,
        source: Optional[SourceTypeEnum] = None,
        local_vars_configuration=None,
    ):  # noqa: E501
        """ContentItem - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._categories = None
        self._content_uri = None
        self._label = None
        self._source = None
        self.discriminator = None

        if categories is not None:
            self.categories = categories
        self.content_uri = content_uri
        self.label = label
        self.source = source

    @property
    def categories(self):
        # type: () -> List[str]
        """Gets the categories of this ContentItem.  # noqa: E501


        :return: The categories of this ContentItem.  # noqa: E501
        :rtype: List[str]
        """
        return self._categories

    @categories.setter
    def categories(self, categories):
        # type: (list[str]) -> None
        """Sets the categories of this ContentItem.


        :param categories: The categories of this ContentItem.  # noqa: E501
        :type categories: list[str]
        :rtype: None
        """
        allowed_values = ["music", "movie", "tv", "hdmi", "app"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and not set(
            categories
        ).issubset(
            set(allowed_values)
        ):  # noqa: E501
            raise ValueError(
                "Invalid values for `categories` [{0}], must be a subset of [{1}]".format(  # noqa: E501
                    ", ".join(
                        map(str, set(categories) - set(allowed_values))
                    ),  # noqa: E501
                    ", ".join(map(str, allowed_values)),
                )
            )

        self._categories = categories

    @property
    def content_uri(self):
        # type: () -> str
        """Gets the content_uri of this ContentItem.  # noqa: E501


        :return: The content_uri of this ContentItem.  # noqa: E501
        :rtype: str
        """
        return self._content_uri

    @content_uri.setter
    def content_uri(self, content_uri):
        # type: (str) -> None
        """Sets the content_uri of this ContentItem.


        :param content_uri: The content_uri of this ContentItem.  # noqa: E501
        :type content_uri: str
        :rtype: None
        """
        if (
            self.local_vars_configuration.client_side_validation and content_uri is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `content_uri`, must not be `None`"
            )  # noqa: E501

        self._content_uri = content_uri

    @property
    def label(self):
        # type: () -> str
        """Gets the label of this ContentItem.  # noqa: E501


        :return: The label of this ContentItem.  # noqa: E501
        :rtype: str
        """
        return self._label

    @label.setter
    def label(self, label):
        # type: (str) -> None
        """Sets the label of this ContentItem.


        :param label: The label of this ContentItem.  # noqa: E501
        :type label: str
        :rtype: None
        """

        self._label = label

    @property
    def source(self):
        # type: () -> SourceTypeEnum
        """Gets the source of this ContentItem.  # noqa: E501


        :return: The source of this ContentItem.  # noqa: E501
        :rtype: SourceTypeEnum
        """
        return self._source

    @source.setter
    def source(self, source):
        # type: (SourceTypeEnum) -> None
        """Sets the source of this ContentItem.


        :param source: The source of this ContentItem.  # noqa: E501
        :type source: SourceTypeEnum
        :rtype: None
        """
        if (
            self.local_vars_configuration.client_side_validation and source is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `source`, must not be `None`"
            )  # noqa: E501

        self._source = source

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
        if not isinstance(other, ContentItem):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ContentItem):
            return True

        return self.to_dict() != other.to_dict()
