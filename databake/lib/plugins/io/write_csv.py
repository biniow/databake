#!/usr/bin/env python
# -*- coding: utf-8 -*-
from databake.lib.plugins import common

__version__ = '1.0.0'
__author__ = 'Wojciech Biniek'
__author_email__ = 'wojtek.biniek@gmail.com'
__maintainer__ = 'Wojciech Biniek'
__maintainer_email__ = 'wojtek.biniek@gmail.com'
__plugin_name__ = 'Read CSV'
__input_pins__ = ('input_df', )
__output_pins__ = ()
__parameters__ = {
    'filepath': {'type': str},
    'sep': {'type': str, 'default': ','}
}


def run(**kwargs):
    input_pins, params = common.clean_data(__input_pins__, __parameters__, **kwargs)

    input_df = input_pins['input_df']
    params['path_or_buf'] = params['filepath']
    del params['filepath']
    input_df.to_csv(**params)
