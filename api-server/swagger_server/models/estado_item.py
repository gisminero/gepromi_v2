# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class EstadoItem(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, id: str=None, name: str=None, release_date: datetime=None):  # noqa: E501
        """EstadoItem - a model defined in Swagger

        :param id: The id of this EstadoItem.  # noqa: E501
        :type id: str
        :param name: The name of this EstadoItem.  # noqa: E501
        :type name: str
        :param release_date: The release_date of this EstadoItem.  # noqa: E501
        :type release_date: datetime
        """
        self.swagger_types = {
            'id': str,
            'name': str,
            'release_date': datetime
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'release_date': 'releaseDate'
        }

        self._id = id
        self._name = name
        self._release_date = release_date

    @classmethod
    def from_dict(cls, dikt) -> 'EstadoItem':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The EstadoItem of this EstadoItem.  # noqa: E501
        :rtype: EstadoItem
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self) -> str:
        """Gets the id of this EstadoItem.


        :return: The id of this EstadoItem.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id: str):
        """Sets the id of this EstadoItem.


        :param id: The id of this EstadoItem.
        :type id: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def name(self) -> str:
        """Gets the name of this EstadoItem.


        :return: The name of this EstadoItem.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this EstadoItem.


        :param name: The name of this EstadoItem.
        :type name: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def release_date(self) -> datetime:
        """Gets the release_date of this EstadoItem.


        :return: The release_date of this EstadoItem.
        :rtype: datetime
        """
        return self._release_date

    @release_date.setter
    def release_date(self, release_date: datetime):
        """Sets the release_date of this EstadoItem.


        :param release_date: The release_date of this EstadoItem.
        :type release_date: datetime
        """

        self._release_date = release_date