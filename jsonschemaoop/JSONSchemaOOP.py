# coding: utf-8

from copy import deepcopy
from jsonschema import Draft4Validator


class JSONType(object):
    type = None

    def __init__(self, *types):
        if types:
            self.type = types

        if isinstance(self.type, (tuple, list)):
            self.type = [
                t.render() if isinstance(t, (JSONObject, JSONArray, JSONSchemaReference)) else t.type
                for t in self.type
            ]

    def render(self):
        return {'type': self.type}


class JSONNumber(JSONType):
    type = 'number'
    minimum = None
    maximum = None
    multiple_of = None

    def __init__(self, minimum=None, maximum=None, multiple_of=None):
        super(JSONNumber, self).__init__()
        if minimum:
            self.minimum = minimum
        if maximum:
            self.maximum = maximum
        if multiple_of:
            self.multiple_of = multiple_of

    def render(self):
        data = super(JSONNumber, self).render()
        if self.minimum:
            data.update(minimum=self.minimum)
        if self.maximum:
            data.update(maximum=self.maximum)
        if self.multiple_of:
            data.update(multipleOf=self.multiple_of)
        return data


class JSONString(JSONType):
    FORMAT_DATETIME = 'date-time'
    FORMAT_EMAIL = 'date-email'
    FORMAT_URI = 'date-uri'
    FORMAT_HOST_NAME = 'host-name'
    FORMAT_IPV4 = 'ipv4'
    FORMAT_IPV6 = 'ipv6'

    type = 'string'
    min_length = None
    max_length = None
    pattern = None
    format = None

    def __init__(self, min_length=None, max_length=None, pattern=None, format=None):
        if min_length:
            self.min_length = min_length
        if max_length:
            self.max_length = max_length
        if pattern:
            self.pattern = pattern
        if format:
            self.format = format

    def render(self):
        data = super(JSONString, self).render()
        if self.min_length:
            data.update(minLength=self.min_length)
        if self.max_length:
            data.update(maxLength=self.max_length)
        if self.pattern:
            data.update(pattern=self.pattern)
        if self.format:
            data.update(format=self.format)
        return data


class JSONSchemaReference(JSONType):
    def __init__(self, type):
        self.type = type

    def render(self):
        return {"$ref": "#/definitions/{}".format(self.type)}


class JSONNull(JSONType):
    type = 'null'


class JSONBoolean(JSONType):
    type = 'boolean'


class JSONArray(JSONType):
    type = 'array'
    unique_items = None
    min_items = None
    max_items = None
    items = []

    def __init__(self, items=[], unique_items=None, min_items=None, max_items=None):
        super(JSONArray, self).__init__()

        self._items = items if items is not None else self.items
        self._unique_items = unique_items if unique_items is not None else self.unique_items
        self._min_items = min_items if min_items is not None else self.min_items
        self._max_items = max_items if max_items is not None else self.max_items

    def render(self):
        obj = super(JSONArray, self).render()

        if self._items:
            obj.update(items=[i.render() for i in self._items])
        if self._unique_items:
            obj.update(uniqueItems=self._unique_items)
        if self._min_items:
            obj.update(minItems=self._min_items)
        if self._max_items:
            obj.update(maxItems=self._max_items)
        return obj


class JSONObject(JSONType):
    type = 'object'
    required = set()
    properties = {}
    min_properties = None
    max_properties = None
    additional_properties = None

    def __init__(self, required=None, properties=None, min_properties=None,
                 max_properties=None, additional_properties=None):
        super(JSONObject, self).__init__()

        self._required = set(required if required is not None else deepcopy(self.required))
        self._properties = properties if properties is not None else deepcopy(self.properties)
        self._min_properties = min_properties if min_properties is not None else deepcopy(self.min_properties)
        self._max_properties = max_properties if max_properties is not None else deepcopy(self.max_properties)

        if additional_properties is not None:
            self._additional_properties = additional_properties
        else:
            self._additional_properties = deepcopy(self.additional_properties)

    def get_required(self):
        """
        Required must be a SET, because this function is called 2 times.
        On child-classes and in the render-function.

        Remove must not raise errors.
        Add elements must prevent duplicate items.

        Use `discard` to safe remove element from set even if it not exists
        Use `add` to safe add element to set even if it exists

        > def get_required(self):
        >     required = super(self.__class__, self).get_required()
        >     required.discard('OLD_ELEMENT')
        >     required.add('NEW_ELEMENT')
        >     return required

        """
        return self._required

    def get_properties(self):
        """
        Properties is a dict, because this function is called 2 times.
        On child-classes and in the render-function.

        Remove must not raise errors.
        Add elements must prevent duplicate items.

        Use `pop` to safe remove element from dict even if it not exists
        Use `update` to safe add element to dict even if it exists

        > def get_properties(self):
        >     properties = super(self.__class__, self).get_properties()
        >     properties.pop('OLD_ELEMENT', None)
        >     properties.update(NEW_ELEMENT=None)
        >     return properties

        """
        return self._properties

    def render(self):
        obj = super(JSONObject, self).render()

        if self._properties:
            obj.update(
                properties={key: value.render() for key, value in self.get_properties().items()}
            )
        if self._required:
            obj.update(required=self.get_required())
        if self._min_properties:
            obj.update(minProperties=self._min_properties)
        if self._max_properties:
            obj.update(maxProperties=self._max_properties)
        if self._additional_properties is not None:
            obj.update(additionalProperties=self._additional_properties)

        return obj


class JSONSchema(JSONObject):
    schema = 'http://json-schema.org/draft-04/schema#'
    definitions = {}

    def render(self):
        schema = super(JSONSchema, self).render()
        schema.update(schema=self.schema)
        if self.definitions:
            schema.update(
                definitions={key: value.render() for key, value in self.definitions.items()})
        return schema

    def validate(self, data):
        Draft4Validator(self.render()).validate(data)
