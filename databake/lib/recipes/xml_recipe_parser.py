#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml

from databake.lib.recipes.exceptions import ParserError
from databake.lib.recipes.recipe import Recipe
from databake.lib.recipes.recipe_parser import RecipeParser


class XmlRecipeParser(RecipeParser):
    def __init__(self, recipe_path):
        super().__init__(recipe_path)

    def parse(self, raw_data=False):
        etree = xml.etree.ElementTree.parse(self.recipe_path)
        data_dict = self._etree_to_dict(etree)
        if raw_data:
            return data_dict
        return Recipe(data_dict)

    def _etree_to_dict(self, etree):
        name = etree.get('name')
        nodes_xml = etree.findall('node')
        connections_xml = etree.findall('connection')

        return {'graph': {
            'name': name,
            'nodes': self._parse_nodes(nodes_xml),
            'connections': self._parse_connections(connections_xml)
        }}

    def _parse_nodes(self, nodes):
        result = []
        for node in nodes:
            parameters = {}

            for param in node.findall('param'):
                parameters[param.get('name')] = param.get('value')

            result.append({
                'name': node.get('name'),
                'id': node.get('id'),
                'plugin_name': node.get('plugin_name'),
                'parameters': parameters
            })
        return result

    def _parse_connections(self, connections):
        result = []
        for connection in connections:
            from_pin = connection.findall('from_pin')
            to_pin = connection.findall('to_pin')

            if len(from_pin) != 1 or len(to_pin) != 1:
                raise ParserError(f'{connection} has invalid structure')

            result.append({
                'name': connection.get('name'),
                'from_pin': {
                    'node': from_pin[0].get('node'),
                    'pin': from_pin[0].get('pin')
                },
                'to_pin': {
                    'node': to_pin[0].get('node'),
                    'pin': to_pin[0].get('pin')
                }
            })
        return result