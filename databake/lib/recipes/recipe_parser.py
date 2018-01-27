#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import pickle

from databake.lib.recipes.exceptions import ParserError
from databake.lib.recipes.recipe import Recipe


class RecipeParser:
    def __init__(self, recipe_path):
        if not os.path.exists(recipe_path):
            raise ParserError(f'{recipe_path} does not exist')

        self.recipe_path = recipe_path

    def parse(self):
        with open(self.recipe_path, 'rb') as recipe_file:
            raw_data = pickle.loads(recipe_file.read())
        return Recipe(raw_data)
