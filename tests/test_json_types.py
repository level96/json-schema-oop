# coding: utf-8

import pytest

from JSONSchema import JSONNumber, JSONString, JSONSchemaReference, JSONNull, JSONBoolean, JSONArray, JSONObject


class TestJSONType:
    @pytest.mark.parametrize(('parameters', 'expected'), [
        ({}, {'type': 'number'}),
        ({'minimum': 1}, {'type': 'number', 'minimum': 1}),
        ({'maximum': 2}, {'type': 'number', 'maximum': 2}),
        ({'multiple_of': 2}, {'type': 'number', 'multipleOf': 2}),

        (
            {'minimum': 1, 'maximum': 4, 'multiple_of': 2},
            {'type': 'number', 'minimum': 1, 'maximum': 4, 'multipleOf': 2}
        ),
    ])
    def test_json_number(self, parameters, expected):
        inst = JSONNumber(**parameters)

        inst_obj = inst.render()

        assert inst_obj == expected

    @pytest.mark.parametrize(('parameters', 'expected'), [
        ({}, {'type': 'string'}),
        ({'min_length': 1}, {'type': 'string', 'minLength': 1}),
        ({'max_length': 10}, {'type': 'string', 'maxLength': 10}),
        ({'pattern': '\\d'}, {'type': 'string', 'pattern': '\\d'}),

        (
            {'min_length': 1, 'max_length': 10, 'pattern': '\\d'},
            {'type': 'string', 'minLength': 1, 'maxLength': 10, 'pattern': '\\d'}
        ),
    ])
    def test_json_string(self, parameters, expected):
        inst = JSONString(**parameters)

        inst_obj = inst.render()

        assert inst_obj == expected

    @pytest.mark.parametrize(('parameters', 'expected'), [
        ({}, {'type': 'array', 'items': []}),
        ({'items': [JSONString()]}, {'items': [{'type': 'string'}], 'type': 'array'}),
        ({'unique_items': True}, {'uniqueItems': True, 'type': 'array', 'items': []}),
        ({'min_items': True}, {'minItems': True, 'type': 'array', 'items': []}),
        ({'max_items': True}, {'maxItems': True, 'type': 'array', 'items': []}),

        (
            {'min_items': 1, 'max_items': 10, 'unique_items': True, 'items': [JSONString()]},
            {'minItems': 1, 'maxItems': 10, 'uniqueItems': True, 'items': [{'type': 'string'}], 'type': 'array'}
        ),
    ])
    def test_json_array(self, parameters, expected):
        inst = JSONArray(**parameters)

        inst_obj = inst.render()

        assert inst_obj == expected

    @pytest.mark.parametrize(('parameters', 'expected'), [
        (
            {'properties': {'name': JSONString()}},
            {'type': 'object', 'properties': {'name': {'type': 'string'}}}
        ),
        (
            {'properties': {'name': JSONString()}, 'required': ['name']},
            {'type': 'object', 'properties': {'name': {'type': 'string'}}, 'required': ['name']}
        ),
        (
            {'properties': {'name': JSONString()}, 'min_properties': 1},
            {'type': 'object', 'properties': {'name': {'type': 'string'}}, 'minProperties': 1}
        ),
        (
            {'properties': {'name': JSONString()}, 'max_properties': 10},
            {'type': 'object', 'properties': {'name': {'type': 'string'}}, 'maxProperties': 10}
        ),

        (
            {'properties': {'name': JSONString()}, 'min_properties': 1, 'max_properties': 10},
            {'type': 'object', 'properties': {'name': {'type': 'string'}}, 'minProperties': 1, 'maxProperties': 10}
        ),
    ])
    def test_json_object(self, parameters, expected):
        inst = JSONObject(**parameters)

        inst_obj = inst.render()

        assert inst_obj == expected

    def test_json_schema_reference(self):
        inst = JSONSchemaReference('my-reference')

        assert inst.render() == {'$ref': '#/definitions/my-reference'}

    def test_json_null(self):
        inst = JSONNull()

        assert inst.render() == {'type': 'null'}

    def test_json_boolean(self):
        inst = JSONBoolean()

        assert inst.render() == {'type': 'boolean'}

