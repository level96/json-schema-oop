# coding: utf-8


class JSONType(object):
    type = None

    def __init__(self, *types):
        if types:
            self.type = types

        if isinstance(self.type, (tuple, list)):
            self.type = [t.type for t in self.type]

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
    type = 'string'
    min_length = None
    max_length = None
    pattern = None

    def __init__(self, min_length=None, max_length=None, pattern=None):
        if min_length:
            self.min_length = min_length
        if max_length:
            self.max_length = max_length
        if pattern:
            self.pattern = pattern

    def render(self):
        data = super(JSONString, self).render()
        if self.min_length:
            data.update(minLength=self.min_length)
        if self.max_length:
            data.update(maxLength=self.max_length)
        if self.pattern:
            data.update(pattern=self.pattern)
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

        if items:
            self.items = items
        if unique_items:
            self.unique_items = unique_items
        if min_items:
            self.min_items = min_items
        if max_items:
            self.max_items = max_items

    def render(self):
        obj = super(JSONArray, self).render()
        obj.update({
            'items': [i.render() for i in self.items]
        })

        if self.unique_items:
            obj.update(uniqueItems=self.unique_items)
        if self.min_items:
            obj.update(minItems=self.min_items)
        if self.max_items:
            obj.update(maxItems=self.max_items)
        return obj


class JSONObject(JSONType):
    type = 'object'
    required = []
    properties = {'type': JSONNull()}
    min_properties = None
    max_properties = None

    def __init__(self, required=None, properties=None, min_properties=None, max_properties=None):
        super(JSONObject, self).__init__()
        if required:
            self.required = required
        if properties:
            self.properties = properties
        if min_properties:
            self.min_properties = min_properties
        if max_properties:
            self.max_properties = max_properties

        required_add = self.required_add()
        required_remove = self.required_remove()

        if required_add:
            self.required = list(set(self.required + required_add))
        if required_remove:
            self.required = list(set(self.required) - set(required_remove))

        properties_add = self.properties_add()
        properties_remove = self.properties_remove()

        if properties_add:
            self.properties.update(properties_add)
        if properties_remove:
            for k in properties_remove:
                self.properties.pop(k)

    def required_add(self):
        return []

    def required_remove(self):
        return []

    def properties_add(self):
        return {}

    def properties_remove(self):
        return []

    def render(self):
        obj = super(JSONObject, self).render()
        obj.update(properties={key: value.render() for key, value in self.properties.items()})

        if self.required:
            obj.update(required=self.required)
        if self.min_properties:
            obj.update(minProperties=self.min_properties)
        if self.max_properties:
            obj.update(maxProperties=self.max_properties)

        return obj


class JSONSchema(JSONObject):
    schema = 'http://json-schema.org/draft-04/schema#'
    definitions = {}

    def render(self):
        schema = super(JSONSchema, self).render()
        schema.update(schema=self.schema)
        if self.definitions:
            schema.update(definitions={key: value.render() for key, value in self.definitions.items()})
        return schema
