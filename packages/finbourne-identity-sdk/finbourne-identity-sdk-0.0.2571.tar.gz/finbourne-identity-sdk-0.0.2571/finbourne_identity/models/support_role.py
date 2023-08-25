# coding: utf-8

"""
    FINBOURNE Identity Service API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 0.0.2571
    Contact: info@finbourne.com
    Generated by: https://openapi-generator.tech
"""


try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec
import pprint
import re  # noqa: F401
import six

from finbourne_identity.configuration import Configuration


class SupportRole(object):
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
      required_map (dict): The key is attribute name
                           and the value is whether it is 'required' or 'optional'.
    """
    openapi_types = {
        'label': 'str',
        'description': 'str',
        'role_identifier': 'dict(str, str)',
        'internal_identifier': 'str'
    }

    attribute_map = {
        'label': 'label',
        'description': 'description',
        'role_identifier': 'roleIdentifier',
        'internal_identifier': 'internalIdentifier'
    }

    required_map = {
        'label': 'optional',
        'description': 'optional',
        'role_identifier': 'optional',
        'internal_identifier': 'optional'
    }

    def __init__(self, label=None, description=None, role_identifier=None, internal_identifier=None, local_vars_configuration=None):  # noqa: E501
        """SupportRole - a model defined in OpenAPI"
        
        :param label: 
        :type label: str
        :param description: 
        :type description: str
        :param role_identifier: 
        :type role_identifier: dict(str, str)
        :param internal_identifier: 
        :type internal_identifier: str

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._label = None
        self._description = None
        self._role_identifier = None
        self._internal_identifier = None
        self.discriminator = None

        self.label = label
        self.description = description
        self.role_identifier = role_identifier
        self.internal_identifier = internal_identifier

    @property
    def label(self):
        """Gets the label of this SupportRole.  # noqa: E501


        :return: The label of this SupportRole.  # noqa: E501
        :rtype: str
        """
        return self._label

    @label.setter
    def label(self, label):
        """Sets the label of this SupportRole.


        :param label: The label of this SupportRole.  # noqa: E501
        :type label: str
        """

        self._label = label

    @property
    def description(self):
        """Gets the description of this SupportRole.  # noqa: E501


        :return: The description of this SupportRole.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this SupportRole.


        :param description: The description of this SupportRole.  # noqa: E501
        :type description: str
        """

        self._description = description

    @property
    def role_identifier(self):
        """Gets the role_identifier of this SupportRole.  # noqa: E501


        :return: The role_identifier of this SupportRole.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._role_identifier

    @role_identifier.setter
    def role_identifier(self, role_identifier):
        """Sets the role_identifier of this SupportRole.


        :param role_identifier: The role_identifier of this SupportRole.  # noqa: E501
        :type role_identifier: dict(str, str)
        """

        self._role_identifier = role_identifier

    @property
    def internal_identifier(self):
        """Gets the internal_identifier of this SupportRole.  # noqa: E501


        :return: The internal_identifier of this SupportRole.  # noqa: E501
        :rtype: str
        """
        return self._internal_identifier

    @internal_identifier.setter
    def internal_identifier(self, internal_identifier):
        """Sets the internal_identifier of this SupportRole.


        :param internal_identifier: The internal_identifier of this SupportRole.  # noqa: E501
        :type internal_identifier: str
        """

        self._internal_identifier = internal_identifier

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
        if not isinstance(other, SupportRole):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, SupportRole):
            return True

        return self.to_dict() != other.to_dict()
