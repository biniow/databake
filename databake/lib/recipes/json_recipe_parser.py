#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from databake.lib.recipes.recipe import Recipe
from databake.lib.recipes.recipe_parser import RecipeParser


class JsonRecipeParser(RecipeParser):
    def __init__(self, recipe_path):
        super().__init__(recipe_path)

    def parse(self, raw_data=False):
        with open(self.recipe_path) as json_file:
            data_dict = json.loads(json_file.read())
        if raw_data:
            return data_dict
        return Recipe(data_dict)
