#!/usr/bin/env python
# -*- coding: utf-8 -*-
import importlib
from unittest import TestCase

from mock import mock, mock_open

from databake.lib.recipes.exceptions import ParserError
from databake.lib.recipes.recipe import Recipe
from databake.lib.recipes.recipe_parser import RecipeParser


class TestRecipeParser(TestCase):
    @mock.patch('os.path.exists', return_value=True)
    def test_recipeParser_recipeExistInPath_properlyCreated(self, os_mock):
        # Arrange
        recipe_path = '/tmp/recipe'

        # Act
        recipe_parser = RecipeParser(recipe_path)

        # Assert
        self.assertEqual(recipe_parser.recipe_path, recipe_path)

    @mock.patch('os.path.exists', return_value=False)
    def test_recipeParser_recipeDoesntExistInPath_raiseParserError(self, os_mock):
        # Arrange
        recipe_path = 'invalid_Path_to_recipe'

        # Act / Assert
        self.assertRaises(ParserError, RecipeParser, recipe_path)

    @mock.patch('pickle.loads')
    @mock.patch('builtins.open', new_callable=mock_open)
    @mock.patch('os.path.exists', return_value=True)
    def test_parse_validReadFromFile_parsedRecipeReturned(self, os_path_mock, open_mock, pickle_mock):
        # Arrange
        recipe_parser = RecipeParser('valid/mock/path/to/recipe')
        pickle_mock.return_value = {
            'graph': {
                'name': 'test',
                'nodes': [],
                'connections': []
            }
        }

        # Act
        returned_value = recipe_parser.parse()

        # Assert
        self.assertIsInstance(returned_value, Recipe)
