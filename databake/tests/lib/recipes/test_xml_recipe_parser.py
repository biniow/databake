#!/usr/bin/env python
from unittest import TestCase


# -*- coding: utf-8 -*-
from xml.etree.ElementTree import Element, tostring

from mock import mock

from databake.lib.recipes.recipe import Recipe
from databake.lib.recipes.xml_recipe_parser import XmlRecipeParser


def dict_to_xml(tag, d):
    elem = Element(tag)
    if isinstance(d, dict):
        for k, v in d.items():
            child = dict_to_xml(k, v)
            elem.append(child)
    elif isinstance(d, list) or isinstance(d, tuple):
        for k in d:
            child = dict_to_xml(tag[:-1], k)
            elem.append(child)
    else:
        elem.text = str(d)
    return elem


class TestXmlRecipeParser(TestCase):
    def setUp(self):
        self.example_data = {
            'name': 'name of graph',
            'nodes': [
                {
                    'name': 'node1',
                    'id': 1,
                    'plugin_name': 'name of plugin',
                    'parameters': {
                        'param1': 'value1',
                        'param2': 'value2'
                    }
                },
                {
                    'name': 'node2',
                    'id': 2,
                    'plugin_name': 'name of plugin',
                    'parameters': {
                        'param3': 'value3',
                        'param4': 'value4'
                    }
                }
            ],
            'connections': [
                {
                    'name': 'connection1',
                    'from_pin': {
                        'node': 1,
                        'pin': 'output'
                    },
                    'to_pin': {
                        'node': 2,
                        'pin': 'input'
                    }
                }
            ]
        }

    @mock.patch('databake.lib.recipes.recipe_parser.RecipeParser.__init__')
    def test_xmlRecipeParser_normalCreation_superCalledOnce(self, init_mock):
        # Arrange / Act
        XmlRecipeParser('dummy/path')
        # Assert
        self.assertEqual(init_mock.call_count, 1)

    @mock.patch('xml.etree.ElementTree.parse')
    @mock.patch('databake.lib.recipes.recipe_parser.RecipeParser.__init__')
    def test_parse_normalExecution_returnParsedRecipe(self, init_mock, parse_mock):
        # Arrange
        xml_parser = XmlRecipeParser('dummy/path')
        parse_mock.return_value = dict_to_xml('graph', self.example_data)

        # Act
        returned_value = xml_parser.parse()

        # Assert
        self.assertIsInstance(returned_value, Recipe)


