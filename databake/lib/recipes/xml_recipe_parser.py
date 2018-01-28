#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml
from xml.etree.ElementTree import tostring

from databake.lib.recipes.recipe import Recipe
from databake.lib.recipes.recipe_parser import RecipeParser


class XmlRecipeParser(RecipeParser):
    def __init__(self, recipe_path):
        super().__init__(recipe_path)

    def parse(self):
        etree = xml.etree.ElementTree.parse()
        raw_data = self._etree_to_dict(etree)
        return Recipe(raw_data)

    def _etree_to_dict(self, etree):
        name = etree.findall('name')[0].text
        nodes = []
        connections = []
        parameters = {}

        for tag in etree.findall('nodes')[0]:
            node = {}
            for child in tag:
                parameter = {}
                for parameter_data in child:
                    parameter[parameter_data.tag] = parameter_data.text
                node[child.tag] = child.text if child.text is not None else parameter
            nodes.append(node)

        for tag in etree.findall('connections')[0]:
            connection = {}
            for child in tag:
                pin = {}
                for pin_data in child:
                    pin[pin_data.tag] = pin_data.text
                connection[child.tag] = child.text if child.text is not None else pin
            connections.append(connection)

        for tag in etree.findall('parameters'):
            for child in tag:
                parameters[child.tag] = child.text

        return {'graph': {
            'name': name,
            'nodes': nodes,
            'connections': connections
        }}