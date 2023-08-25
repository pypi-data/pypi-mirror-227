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

from mozart_api.models.action import Action

from mozart_api.configuration import Configuration


class SceneTriggerBaseProperties(object):
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
    openapi_types = {"action_list": "list[Action]", "scene_list": "list[str]"}

    attribute_map = {"action_list": "actionList", "scene_list": "sceneList"}

    def __init__(
        self,
        action_list: Optional[List[Action]] = None,
        scene_list: Optional[List[str]] = None,
        local_vars_configuration=None,
    ):  # noqa: E501
        """SceneTriggerBaseProperties - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._action_list = None
        self._scene_list = None
        self.discriminator = None

        if action_list is not None:
            self.action_list = action_list
        if scene_list is not None:
            self.scene_list = scene_list

    @property
    def action_list(self):
        # type: () -> List[Action]
        """Gets the action_list of this SceneTriggerBaseProperties.  # noqa: E501

        An ordered list of Actions to run on the product  # noqa: E501

        :return: The action_list of this SceneTriggerBaseProperties.  # noqa: E501
        :rtype: List[Action]
        """
        return self._action_list

    @action_list.setter
    def action_list(self, action_list):
        # type: (list[Action]) -> None
        """Sets the action_list of this SceneTriggerBaseProperties.

        An ordered list of Actions to run on the product  # noqa: E501

        :param action_list: The action_list of this SceneTriggerBaseProperties.  # noqa: E501
        :type action_list: list[Action]
        :rtype: None
        """

        self._action_list = action_list

    @property
    def scene_list(self):
        # type: () -> List[str]
        """Gets the scene_list of this SceneTriggerBaseProperties.  # noqa: E501

        A list of scenes  # noqa: E501

        :return: The scene_list of this SceneTriggerBaseProperties.  # noqa: E501
        :rtype: List[str]
        """
        return self._scene_list

    @scene_list.setter
    def scene_list(self, scene_list):
        # type: (list[str]) -> None
        """Sets the scene_list of this SceneTriggerBaseProperties.

        A list of scenes  # noqa: E501

        :param scene_list: The scene_list of this SceneTriggerBaseProperties.  # noqa: E501
        :type scene_list: list[str]
        :rtype: None
        """

        self._scene_list = scene_list

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
        if not isinstance(other, SceneTriggerBaseProperties):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, SceneTriggerBaseProperties):
            return True

        return self.to_dict() != other.to_dict()
