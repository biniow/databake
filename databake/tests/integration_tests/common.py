#!/usr/bin/env python
# -*- coding: utf-8 -*-
from databake.lib.graph.graph import Graph
from databake.lib.recipes.json_recipe_parser import JsonRecipeParser
from databake.lib.recipes.recipe_parser import RecipeParser
from databake.lib.recipes.xml_recipe_parser import XmlRecipeParser


def get_graph(file_path):
    if file_path.endswith('.xml'):
        parser = XmlRecipeParser(file_path)
    elif file_path.endswith('.json'):
        parser = JsonRecipeParser(file_path)
    elif file_path.endswith('.databake'):
        parser = RecipeParser(file_path)
    else:
        raise Exception('Input file not supported! Test FAILED')

    return Graph(parser.parse())
