# coding: utf-8

"""
    FINBOURNE Access Management API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 0.0.3212
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

from finbourne_access.configuration import Configuration


class AsAtRelative(object):
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
        'date': 'PointInTimeSpecification',
        'adjustment': 'int',
        'unit': 'DateUnit',
        'relative_to_date_time': 'RelativeToDateTime'
    }

    attribute_map = {
        'date': 'date',
        'adjustment': 'adjustment',
        'unit': 'unit',
        'relative_to_date_time': 'relativeToDateTime'
    }

    required_map = {
        'date': 'optional',
        'adjustment': 'optional',
        'unit': 'optional',
        'relative_to_date_time': 'optional'
    }

    def __init__(self, date=None, adjustment=None, unit=None, relative_to_date_time=None, local_vars_configuration=None):  # noqa: E501
        """AsAtRelative - a model defined in OpenAPI"
        
        :param date: 
        :type date: finbourne_access.PointInTimeSpecification
        :param adjustment: 
        :type adjustment: int
        :param unit: 
        :type unit: finbourne_access.DateUnit
        :param relative_to_date_time: 
        :type relative_to_date_time: finbourne_access.RelativeToDateTime

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._date = None
        self._adjustment = None
        self._unit = None
        self._relative_to_date_time = None
        self.discriminator = None

        if date is not None:
            self.date = date
        if adjustment is not None:
            self.adjustment = adjustment
        if unit is not None:
            self.unit = unit
        if relative_to_date_time is not None:
            self.relative_to_date_time = relative_to_date_time

    @property
    def date(self):
        """Gets the date of this AsAtRelative.  # noqa: E501


        :return: The date of this AsAtRelative.  # noqa: E501
        :rtype: finbourne_access.PointInTimeSpecification
        """
        return self._date

    @date.setter
    def date(self, date):
        """Sets the date of this AsAtRelative.


        :param date: The date of this AsAtRelative.  # noqa: E501
        :type date: finbourne_access.PointInTimeSpecification
        """

        self._date = date

    @property
    def adjustment(self):
        """Gets the adjustment of this AsAtRelative.  # noqa: E501


        :return: The adjustment of this AsAtRelative.  # noqa: E501
        :rtype: int
        """
        return self._adjustment

    @adjustment.setter
    def adjustment(self, adjustment):
        """Sets the adjustment of this AsAtRelative.


        :param adjustment: The adjustment of this AsAtRelative.  # noqa: E501
        :type adjustment: int
        """

        self._adjustment = adjustment

    @property
    def unit(self):
        """Gets the unit of this AsAtRelative.  # noqa: E501


        :return: The unit of this AsAtRelative.  # noqa: E501
        :rtype: finbourne_access.DateUnit
        """
        return self._unit

    @unit.setter
    def unit(self, unit):
        """Sets the unit of this AsAtRelative.


        :param unit: The unit of this AsAtRelative.  # noqa: E501
        :type unit: finbourne_access.DateUnit
        """

        self._unit = unit

    @property
    def relative_to_date_time(self):
        """Gets the relative_to_date_time of this AsAtRelative.  # noqa: E501


        :return: The relative_to_date_time of this AsAtRelative.  # noqa: E501
        :rtype: finbourne_access.RelativeToDateTime
        """
        return self._relative_to_date_time

    @relative_to_date_time.setter
    def relative_to_date_time(self, relative_to_date_time):
        """Sets the relative_to_date_time of this AsAtRelative.


        :param relative_to_date_time: The relative_to_date_time of this AsAtRelative.  # noqa: E501
        :type relative_to_date_time: finbourne_access.RelativeToDateTime
        """

        self._relative_to_date_time = relative_to_date_time

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
        if not isinstance(other, AsAtRelative):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AsAtRelative):
            return True

        return self.to_dict() != other.to_dict()
