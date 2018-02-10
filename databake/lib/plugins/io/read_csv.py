#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd

from databake.lib.plugins import common

__version__ = '1.0.0'
__author__ = 'Wojciech Biniek'
__author_email__ = 'wojtek.biniek@gmail.com'
__maintainer__ = 'Wojciech Biniek'
__maintainer_email__ = 'wojtek.biniek@gmail.com'
__plugin_name__ = 'Read CSV'
__input_pins__ = ()
__output_pins__ = ('output_df', )
__parameters__ = {
    'filepath': {'type': str},
    'delimiter': {'type': str, 'default': ','}
}


def run(**kwargs):
    _, params = common.clean_data(__input_pins__, __parameters__, **kwargs)

    filepath = params['filepath']
    del params['filepath']

    return {
        'output_df': pd.read_csv(filepath, **params)
    }
