Write DRY JSON-Schema with Python classes, inherit classes for new JSON-Schema-Version   

This supports only jsonschema Draft4Validator at this time

[![Build Status](https://travis-ci.org/level96/json-schema-oop.svg?branch=master)](https://travis-ci.org/level96/json-schema-oop)
[![Coverage Status](https://coveralls.io/repos/github/level96/json-schema-oop/badge.svg?branch=master)](https://coveralls.io/github/level96/json-schema-oop?branch=master)



# Install 

    pip install https://github.com/level96/json-schema-oop.git#egg=jsonschemaoop
    
# Example

We want to validate an address-schema with following data


```python
location = {
    'address': {
        'street': 'john doe street', 
        'street_number': '12 a', 
        'zip': '12345',
        'city': 'Berlin'
    }
}
```


Create a schema object

```python
from JSONSchemaOOP import JSONObject, JSONString, JSONType, JSONNumber 

class AddressJSONSchemaObject(JSONObject):
    required = ['street', 'street_number', 'zip', 'city']
    properties = {
        'street': JSONString(),
        'street_number': JSONString(),
        'zip': JSONType(JSONNumber(), JSONString),
        'city': JSONString(),
    }
```

Create a schema, put SchemaObject to the definitions or properties 


```python
from JSONSchemaOOP import JSONSchema, JSONSchemaReference

class AddressSchema(JSONSchema):
    properties = {
        'address': JSONSchemaReference('address')
    }
    definitions = {
        'address': AddressJSONSchemaObject()
    }
```

Now validate the `location` object.
This uses `Draft4Validator(obj).validate(data)`. It returns nothing on success and raises `jsonschema.exceptions.ValidationError` if Schema doesn't match

```python
schema = AddressSchema()

schema.validate(location)
```


Now Address-Schema has changed. `city` is renamed to `location` and a new array-field `staff` is added.
Let's reflect this to our `AddressJSONSchemaObject` and add a new Version `AddressJSONSchemaObjectV2`

```Python
location = {
    'address': {
        'street': 'john doe street', 
        'street_number': '12 a', 
        'zip': '12345',
        'location': 'Berlin',
        'staff': ['John']
    }
}
```

```python
class AddressJSONSchemaObjectV2(AddressJSONSchemaObject):
    def required_remove(self):
        return super(AddressJSONSchemaObjectV2, self).required_add() + ['city']

    def properties_remove(self):
        return super(AddressJSONSchemaObjectV2, self).properties_remove() + ['city']
       
    def required_add(self):
        return super(AddressJSONSchemaObjectV2, self).required_add() + ['location']

    def properties_add(self):
        obj = super(AddressJSONSchemaObjectV2, self).properties_add()
        obj.update(
            location=JSONString(),
            staff=JSONSchemaOOP.JSONArray(
                min_items=1,
                items=[JSONSchemaOOP.JSONString()]
            )
        )
        return obj
```

Now update `AddressSchema`

```python
class AddressSchemaV2(AddressSchema):
    definitions = {
        'address': AddressJSONSchemaObjectV2()
    }
```
