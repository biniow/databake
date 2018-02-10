#!/usr/bin/env python
# -*- coding: utf-8 -*-
import importlib
from tempfile import NamedTemporaryFile
from unittest import TestCase

import os
import pandas as pd
from pandas.util.testing import assert_frame_equal


class TestPluginReadCSV(TestCase):
    def setUp(self):
        self.plugin_name = 'databake.lib.plugins.core.join'

        self.left_df = pd.DataFrame({'a': [1, 2, 3, 4], 'b': [5, 6, 7, 8]})
        self.right_df = pd.DataFrame({'a': [1, 2, 3, 4], 'c': ['test1', 'test2', 'test3', 'test4']})

    def test_run_joinDataFrames_ProperlyJoined(self):
        parameters = {
            'on': 'a',
            'how': 'left'
        }

        plugin = importlib.import_module(self.plugin_name)
        input_pins = {
            'left_df': self.left_df,
            'right_df': self.right_df
        }

        expected_result = pd.DataFrame({
            'a': [1, 2, 3, 4],
            'b': [5, 6, 7, 8],
            'c': ['test1', 'test2', 'test3', 'test4']
        })

        result = plugin.run(input_pins=input_pins, parameters=parameters)

        assert_frame_equal(expected_result, result['output_df'])

