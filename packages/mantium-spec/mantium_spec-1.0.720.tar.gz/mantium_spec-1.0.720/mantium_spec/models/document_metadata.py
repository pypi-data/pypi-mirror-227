# coding: utf-8

"""
    Mantium API

    Mantium API Documentation  # noqa: E501

    The version of the OpenAPI document: 1.0.720
    Generated by: https://openapi-generator.tech
"""


try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec
import pprint
import re  # noqa: F401
import six

from mantium_spec.configuration import Configuration


class DocumentMetadata(object):
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
        'sync_file_id': 'str'
    }

    attribute_map = {
        'sync_file_id': 'sync_file_id'
    }

    def __init__(self, sync_file_id=None, local_vars_configuration=None):  # noqa: E501
        """DocumentMetadata - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._sync_file_id = None
        self.discriminator = None

        self.sync_file_id = sync_file_id

    @property
    def sync_file_id(self):
        """Gets the sync_file_id of this DocumentMetadata.  # noqa: E501


        :return: The sync_file_id of this DocumentMetadata.  # noqa: E501
        :rtype: str
        """
        return self._sync_file_id

    @sync_file_id.setter
    def sync_file_id(self, sync_file_id):
        """Sets the sync_file_id of this DocumentMetadata.


        :param sync_file_id: The sync_file_id of this DocumentMetadata.  # noqa: E501
        :type sync_file_id: str
        """
        if self.local_vars_configuration.client_side_validation and sync_file_id is None:  # noqa: E501
            raise ValueError("Invalid value for `sync_file_id`, must not be `None`")  # noqa: E501

        self._sync_file_id = sync_file_id

    def to_dict(self, serialize=False):
        """Returns the model properties as a dict"""
        result = {}

        def convert(x):
            if hasattr(x, "to_dict"):
                args = getfullargspec(x.to_dict).args
                if len(args) == 1:
                    return x.to_dict()
                else:
                    return x.to_dict(serialize)
            else:
                return x

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.attribute_map.get(attr, attr) if serialize else attr
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: convert(x),
                    value
                ))
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], convert(item[1])),
                    value.items()
                ))
            else:
                result[attr] = convert(value)

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, DocumentMetadata):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, DocumentMetadata):
            return True

        return self.to_dict() != other.to_dict()
