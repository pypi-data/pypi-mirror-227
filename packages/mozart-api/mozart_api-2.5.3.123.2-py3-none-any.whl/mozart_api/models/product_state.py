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

from mozart_api.models.tv_state import TvState
from mozart_api.models.software_update_state import SoftwareUpdateState
from mozart_api.models.power_state_enum import PowerStateEnum
from mozart_api.models.sound_settings import SoundSettings
from mozart_api.models.playback_state import PlaybackState
from mozart_api.models.volume_state import VolumeState
from mozart_api.models.microphones_state import MicrophonesState
from mozart_api.models.source import Source

from mozart_api.configuration import Configuration


class ProductState(object):
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
        "microphones": "MicrophonesState",
        "playback": "PlaybackState",
        "power_state": "PowerStateEnum",
        "software_update_state": "SoftwareUpdateState",
        "sound_settings": "SoundSettings",
        "source": "Source",
        "tv": "TvState",
        "volume": "VolumeState",
    }

    attribute_map = {
        "microphones": "microphones",
        "playback": "playback",
        "power_state": "powerState",
        "software_update_state": "softwareUpdateState",
        "sound_settings": "soundSettings",
        "source": "source",
        "tv": "tv",
        "volume": "volume",
    }

    def __init__(
        self,
        microphones: Optional[MicrophonesState] = None,
        playback: Optional[PlaybackState] = None,
        power_state: Optional[PowerStateEnum] = None,
        software_update_state: Optional[SoftwareUpdateState] = None,
        sound_settings: Optional[SoundSettings] = None,
        source: Optional[Source] = None,
        tv: Optional[TvState] = None,
        volume: Optional[VolumeState] = None,
        local_vars_configuration=None,
    ):  # noqa: E501
        """ProductState - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._microphones = None
        self._playback = None
        self._power_state = None
        self._software_update_state = None
        self._sound_settings = None
        self._source = None
        self._tv = None
        self._volume = None
        self.discriminator = None

        if microphones is not None:
            self.microphones = microphones
        if playback is not None:
            self.playback = playback
        if power_state is not None:
            self.power_state = power_state
        if software_update_state is not None:
            self.software_update_state = software_update_state
        if sound_settings is not None:
            self.sound_settings = sound_settings
        if source is not None:
            self.source = source
        if tv is not None:
            self.tv = tv
        if volume is not None:
            self.volume = volume

    @property
    def microphones(self):
        # type: () -> MicrophonesState
        """Gets the microphones of this ProductState.  # noqa: E501


        :return: The microphones of this ProductState.  # noqa: E501
        :rtype: MicrophonesState
        """
        return self._microphones

    @microphones.setter
    def microphones(self, microphones):
        # type: (MicrophonesState) -> None
        """Sets the microphones of this ProductState.


        :param microphones: The microphones of this ProductState.  # noqa: E501
        :type microphones: MicrophonesState
        :rtype: None
        """

        self._microphones = microphones

    @property
    def playback(self):
        # type: () -> PlaybackState
        """Gets the playback of this ProductState.  # noqa: E501


        :return: The playback of this ProductState.  # noqa: E501
        :rtype: PlaybackState
        """
        return self._playback

    @playback.setter
    def playback(self, playback):
        # type: (PlaybackState) -> None
        """Sets the playback of this ProductState.


        :param playback: The playback of this ProductState.  # noqa: E501
        :type playback: PlaybackState
        :rtype: None
        """

        self._playback = playback

    @property
    def power_state(self):
        # type: () -> PowerStateEnum
        """Gets the power_state of this ProductState.  # noqa: E501


        :return: The power_state of this ProductState.  # noqa: E501
        :rtype: PowerStateEnum
        """
        return self._power_state

    @power_state.setter
    def power_state(self, power_state):
        # type: (PowerStateEnum) -> None
        """Sets the power_state of this ProductState.


        :param power_state: The power_state of this ProductState.  # noqa: E501
        :type power_state: PowerStateEnum
        :rtype: None
        """

        self._power_state = power_state

    @property
    def software_update_state(self):
        # type: () -> SoftwareUpdateState
        """Gets the software_update_state of this ProductState.  # noqa: E501


        :return: The software_update_state of this ProductState.  # noqa: E501
        :rtype: SoftwareUpdateState
        """
        return self._software_update_state

    @software_update_state.setter
    def software_update_state(self, software_update_state):
        # type: (SoftwareUpdateState) -> None
        """Sets the software_update_state of this ProductState.


        :param software_update_state: The software_update_state of this ProductState.  # noqa: E501
        :type software_update_state: SoftwareUpdateState
        :rtype: None
        """

        self._software_update_state = software_update_state

    @property
    def sound_settings(self):
        # type: () -> SoundSettings
        """Gets the sound_settings of this ProductState.  # noqa: E501


        :return: The sound_settings of this ProductState.  # noqa: E501
        :rtype: SoundSettings
        """
        return self._sound_settings

    @sound_settings.setter
    def sound_settings(self, sound_settings):
        # type: (SoundSettings) -> None
        """Sets the sound_settings of this ProductState.


        :param sound_settings: The sound_settings of this ProductState.  # noqa: E501
        :type sound_settings: SoundSettings
        :rtype: None
        """

        self._sound_settings = sound_settings

    @property
    def source(self):
        # type: () -> Source
        """Gets the source of this ProductState.  # noqa: E501


        :return: The source of this ProductState.  # noqa: E501
        :rtype: Source
        """
        return self._source

    @source.setter
    def source(self, source):
        # type: (Source) -> None
        """Sets the source of this ProductState.


        :param source: The source of this ProductState.  # noqa: E501
        :type source: Source
        :rtype: None
        """

        self._source = source

    @property
    def tv(self):
        # type: () -> TvState
        """Gets the tv of this ProductState.  # noqa: E501


        :return: The tv of this ProductState.  # noqa: E501
        :rtype: TvState
        """
        return self._tv

    @tv.setter
    def tv(self, tv):
        # type: (TvState) -> None
        """Sets the tv of this ProductState.


        :param tv: The tv of this ProductState.  # noqa: E501
        :type tv: TvState
        :rtype: None
        """

        self._tv = tv

    @property
    def volume(self):
        # type: () -> VolumeState
        """Gets the volume of this ProductState.  # noqa: E501


        :return: The volume of this ProductState.  # noqa: E501
        :rtype: VolumeState
        """
        return self._volume

    @volume.setter
    def volume(self, volume):
        # type: (VolumeState) -> None
        """Sets the volume of this ProductState.


        :param volume: The volume of this ProductState.  # noqa: E501
        :type volume: VolumeState
        :rtype: None
        """

        self._volume = volume

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
        if not isinstance(other, ProductState):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ProductState):
            return True

        return self.to_dict() != other.to_dict()
