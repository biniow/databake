#!/usr/bin/env python
# -*- coding: utf-8 -*-
import importlib
from tempfile import NamedTemporaryFile
from unittest import TestCase

import os
import pandas as pd
from pandas.util.testing import assert_frame_equal


class TestPluginWriteCSV(TestCase):
    def setUp(self):
        self.plugin_name = 'databake.lib.plugins.io.write_csv'
        self.tmp_file = NamedTemporaryFile(delete=False)
        self.df = pd.DataFrame({'a': [1, 2, 3, 4], 'b': [5, 6, 7, 8]})

    def tearDown(self):
        os.unlink(self.tmp_file.name)

    def test_run_writeValidCsvFile_ProperlyWritten(self):
        input_pins = {
            'input_df': self.df
        }

        parameters = {
            'filepath': self.tmp_file.name,
            'delimiter': ','
        }
        plugin = importlib.import_module(self.plugin_name)
        plugin.run(input_pins=input_pins, parameters=parameters)

        result = pd.read_csv(self.tmp_file.name, index_col=0)
        assert_frame_equal(self.df, result)

