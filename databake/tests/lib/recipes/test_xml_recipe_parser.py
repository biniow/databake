#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase
from xml.etree.ElementTree import fromstring

from mock import mock

from databake.lib.recipes.recipe import Recipe
from databake.lib.recipes.xml_recipe_parser import XmlRecipeParser


class TestXmlRecipeParser(TestCase):
    def setUp(self):
        self.example_data = """
        <graph name="name of graph">
            <node name="node1" id="1" plugin_name="name of plugin">
                    <param name="param1" value="value1" />
                    <param name="param2" value="value2" />
            </node>
            <node name="node2" id="2" plugin_name="name of plugin">
                    <param name="param3" value="value3" />
                    <param name="param4" value="value4" />
            </node>
            
            <connection name="connection1">
                    <from_pin node="1" pin="output" />
                    <to_pin node="2" pin="input" />
            </connection>
        </graph>
        """

        self.parsed_dict_example = {
            'graph': {
                'name': 'name of graph',
                'nodes': [
                    {
                        'name': 'node1',
                        'id': '1',
                        'plugin_name': 'name of plugin',
                        'parameters': {
                            'param1': 'value1',
                            'param2': 'value2'
                        }
                    },
                    {
                        'name': 'node2',
                        'id': '2',
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
                            'node': '1',
                            'pin': 'output'
                        },
                        'to_pin': {
                            'node': '2',
                            'pin': 'input'
                        }
                    }
                ]
            }
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
        xml_parser.recipe_path = 'dummy/path'
        parse_mock.return_value = fromstring(self.example_data)

        # Act
        returned_value = xml_parser.parse()

        # Assert
        self.assertIsInstance(returned_value, Recipe)

    @mock.patch('xml.etree.ElementTree.parse')
    @mock.patch('databake.lib.recipes.recipe_parser.RecipeParser.__init__')
    def test_parse_getRawData_returnedValidData(self, init_mock, parse_mock):
        # Arrange
        xml_parser = XmlRecipeParser('dummy/path')
        xml_parser.recipe_path = 'dummy/path'
        parse_mock.return_value = fromstring(self.example_data)

        # Act
        returned_value = xml_parser.parse(raw_data=True)

        # Assert
        self.maxDiff = None
        self.assertDictEqual(self.parsed_dict_example, returned_value)