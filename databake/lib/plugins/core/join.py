#!/usr/bin/env python
# -*- coding: utf-8 -*-
from databake.lib.plugins import common

__version__ = '1.0.0'
__author__ = 'Wojciech Biniek'
__author_email__ = 'wojtek.biniek@gmail.com'
__maintainer__ = 'Wojciech Biniek'
__maintainer_email__ = 'wojtek.biniek@gmail.com'
__plugin_name__ = 'Join'
__input_pins__ = ('left_df', 'right_df')
__output_pins__ = ('output_df',)
__parameters__ = {
    'on': {'type': object, 'default': None},
    'how': {'type': str, 'default': 'inner'},
    'sort': {'type': bool, 'default': False},
    'left_on': {'type': object, 'default': None},
    'right_on': {'type': object, 'default': None},
    'left_index': {'type': bool, 'default': False},
    'right_index': {'type': bool, 'default': False},
    'suffixes': {'type': tuple, 'default': ('_left', '_right')},
    'copy': {'type': bool, 'default': True},
    'indicator': {'type': bool, 'default': False},
    'validate': {'type': object, 'default': None}
}


def run(**kwargs):
    input_pins, params = common.clean_data(__input_pins__, __parameters__, **kwargs)

    left_df = input_pins['left_df']
    right_df = input_pins['right_df']
    result = left_df.merge(right_df, **params)

    return {
        'output_df': result
    }
