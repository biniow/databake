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
        self.plugin_name = 'databake.lib.plugins.io.read_csv'
        self.tmp_file = NamedTemporaryFile(delete=False)
        self.df = pd.DataFrame({'a': [1, 2, 3, 4], 'b': [5, 6, 7, 8]})
        self.df.to_csv(self.tmp_file.name, index=False)

    def tearDown(self):
        os.unlink(self.tmp_file.name)

    def test_run_readValidCsvFile_ProperlyRead(self):
        parameters = {
            'filepath': self.tmp_file.name,
            'delimiter': ','
        }
        plugin = importlib.import_module(self.plugin_name)
        result = plugin.run(parameters=parameters)
        assert_frame_equal(self.df, result['output_df'])

