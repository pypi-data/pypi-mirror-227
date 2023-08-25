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
from mozart_api.models.rendering_state import RenderingState
from mozart_api.models.source import Source
from mozart_api.models.playback_progress import PlaybackProgress

from mozart_api.configuration import Configuration


class PlaybackState(object):
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
        "metadata": "PlaybackContentMetadata",
        "progress": "PlaybackProgress",
        "source": "Source",
        "state": "RenderingState",
    }

    attribute_map = {
        "metadata": "metadata",
        "progress": "progress",
        "source": "source",
        "state": "state",
    }

    def __init__(
        self,
        metadata: Optional[PlaybackContentMetadata] = None,
        progress: Optional[PlaybackProgress] = None,
        source: Optional[Source] = None,
        state: Optional[RenderingState] = None,
        local_vars_configuration=None,
    ):  # noqa: E501
        """PlaybackState - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._metadata = None
        self._progress = None
        self._source = None
        self._state = None
        self.discriminator = None

        if metadata is not None:
            self.metadata = metadata
        if progress is not None:
            self.progress = progress
        if source is not None:
            self.source = source
        if state is not None:
            self.state = state

    @property
    def metadata(self):
        # type: () -> PlaybackContentMetadata
        """Gets the metadata of this PlaybackState.  # noqa: E501


        :return: The metadata of this PlaybackState.  # noqa: E501
        :rtype: PlaybackContentMetadata
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        # type: (PlaybackContentMetadata) -> None
        """Sets the metadata of this PlaybackState.


        :param metadata: The metadata of this PlaybackState.  # noqa: E501
        :type metadata: PlaybackContentMetadata
        :rtype: None
        """

        self._metadata = metadata

    @property
    def progress(self):
        # type: () -> PlaybackProgress
        """Gets the progress of this PlaybackState.  # noqa: E501


        :return: The progress of this PlaybackState.  # noqa: E501
        :rtype: PlaybackProgress
        """
        return self._progress

    @progress.setter
    def progress(self, progress):
        # type: (PlaybackProgress) -> None
        """Sets the progress of this PlaybackState.


        :param progress: The progress of this PlaybackState.  # noqa: E501
        :type progress: PlaybackProgress
        :rtype: None
        """

        self._progress = progress

    @property
    def source(self):
        # type: () -> Source
        """Gets the source of this PlaybackState.  # noqa: E501


        :return: The source of this PlaybackState.  # noqa: E501
        :rtype: Source
        """
        return self._source

    @source.setter
    def source(self, source):
        # type: (Source) -> None
        """Sets the source of this PlaybackState.


        :param source: The source of this PlaybackState.  # noqa: E501
        :type source: Source
        :rtype: None
        """

        self._source = source

    @property
    def state(self):
        # type: () -> RenderingState
        """Gets the state of this PlaybackState.  # noqa: E501


        :return: The state of this PlaybackState.  # noqa: E501
        :rtype: RenderingState
        """
        return self._state

    @state.setter
    def state(self, state):
        # type: (RenderingState) -> None
        """Sets the state of this PlaybackState.


        :param state: The state of this PlaybackState.  # noqa: E501
        :type state: RenderingState
        :rtype: None
        """

        self._state = state

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
        if not isinstance(other, PlaybackState):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, PlaybackState):
            return True

        return self.to_dict() != other.to_dict()
