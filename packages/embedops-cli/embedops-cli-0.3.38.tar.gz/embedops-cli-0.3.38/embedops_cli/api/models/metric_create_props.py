# coding: utf-8

"""
    EmbedOps API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 1.0.0
    Contact: support@embedops.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six


class MetricCreateProps(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        "ci_run_id": "str",
        "dimensions": "object",
        "name": "str",
        "value": "AnyOfMetricCreatePropsValue",
    }

    attribute_map = {
        "ci_run_id": "ciRunId",
        "dimensions": "dimensions",
        "name": "name",
        "value": "value",
    }

    def __init__(
        self, ci_run_id=None, dimensions=None, name=None, value=None
    ):  # noqa: E501
        """MetricCreateProps - a model defined in Swagger"""  # noqa: E501
        self._ci_run_id = None
        self._dimensions = None
        self._name = None
        self._value = None
        self.discriminator = None
        self.ci_run_id = ci_run_id
        if dimensions is not None:
            self.dimensions = dimensions
        self.name = name
        self.value = value

    @property
    def ci_run_id(self):
        """Gets the ci_run_id of this MetricCreateProps.  # noqa: E501


        :return: The ci_run_id of this MetricCreateProps.  # noqa: E501
        :rtype: str
        """
        return self._ci_run_id

    @ci_run_id.setter
    def ci_run_id(self, ci_run_id):
        """Sets the ci_run_id of this MetricCreateProps.


        :param ci_run_id: The ci_run_id of this MetricCreateProps.  # noqa: E501
        :type: str
        """
        if ci_run_id is None:
            raise ValueError(
                "Invalid value for `ci_run_id`, must not be `None`"
            )  # noqa: E501

        self._ci_run_id = ci_run_id

    @property
    def dimensions(self):
        """Gets the dimensions of this MetricCreateProps.  # noqa: E501


        :return: The dimensions of this MetricCreateProps.  # noqa: E501
        :rtype: object
        """
        return self._dimensions

    @dimensions.setter
    def dimensions(self, dimensions):
        """Sets the dimensions of this MetricCreateProps.


        :param dimensions: The dimensions of this MetricCreateProps.  # noqa: E501
        :type: object
        """

        self._dimensions = dimensions

    @property
    def name(self):
        """Gets the name of this MetricCreateProps.  # noqa: E501


        :return: The name of this MetricCreateProps.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this MetricCreateProps.


        :param name: The name of this MetricCreateProps.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError(
                "Invalid value for `name`, must not be `None`"
            )  # noqa: E501

        self._name = name

    @property
    def value(self):
        """Gets the value of this MetricCreateProps.  # noqa: E501


        :return: The value of this MetricCreateProps.  # noqa: E501
        :rtype: AnyOfMetricCreatePropsValue
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of this MetricCreateProps.


        :param value: The value of this MetricCreateProps.  # noqa: E501
        :type: AnyOfMetricCreatePropsValue
        """
        if value is None:
            raise ValueError(
                "Invalid value for `value`, must not be `None`"
            )  # noqa: E501

        self._value = value

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
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
        if issubclass(MetricCreateProps, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, MetricCreateProps):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
