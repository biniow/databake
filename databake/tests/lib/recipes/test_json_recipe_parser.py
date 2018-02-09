#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase

from mock import mock

from databake.lib.recipes.json_recipe_parser import JsonRecipeParser


class TestJsonRecipeParser(TestCase):

    @mock.patch('databake.lib.recipes.recipe_parser.RecipeParser.__init__')
    def test_xmlRecipeParser_normalCreation_superCalledOnce(self, init_mock):
        # Arrange / Act
        JsonRecipeParser('dummy/path')
        # Assert
        self.assertEqual(init_mock.call_count, 1)