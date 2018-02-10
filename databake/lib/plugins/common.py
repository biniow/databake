#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd


def clean_data(meta_inputs, meta_params, **kwargs):
    input_data = kwargs.get('input_pins', {})
    params = kwargs.get('parameters', {})
    if not isinstance(input_data, dict) or not isinstance(params, dict):
        raise Exception('input_pins and parameters should be dicts of value')

    cleaned_input_data = check_input_data(input_data, meta_inputs)
    cleaned_params = check_params(params, meta_params)

    return cleaned_input_data, cleaned_params


def check_input_data(input_pins, meta):
    cleaned_data = {}
    for required_input in meta:
        data = input_pins.get(required_input, None)
        if data is not None:
            if not isinstance(data, pd.DataFrame):
                raise Exception(f'{required_input} should be type {pd.DataFrame}')
            cleaned_data[required_input] = data
        else:
            raise Exception(f'{required_input} not available')
    return cleaned_data


def check_params(params, meta):
    cleaned_data = {}
    for required_param in meta:
        param = params.get(required_param, None)
        if param is not None:
            valid_type = meta[required_param]['type']
            if not isinstance(param, valid_type):
                raise Exception(f'{required_param} should be {valid_type} not {type(param)}')
            cleaned_data[required_param] = param
        else:
            cleaned_data[required_param] = meta[required_param]['default']
    return cleaned_data
