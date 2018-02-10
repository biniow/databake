#!/usr/bin/env python
# -*- coding: utf-8 -*-
from databake.lib.recipes.exceptions import ParserError


class Recipe:
    def __init__(self, recipe_raw_data):
        recipe_raw_data = recipe_raw_data['graph']
        self.graph_name = recipe_raw_data['name']
        self.nodes = []
        self.connections = []

        for node in recipe_raw_data['nodes']:
            self.nodes.append(_NodeRecipeItem(**node))

        for connection in recipe_raw_data['connections']:
            self.connections.append(_ConnectionRecipeItem(**connection))

        self.check_connections()

    def check_connections(self):
        unique_pins = []
        for connection in self.connections:
            if connection.to_pin not in unique_pins:
                unique_pins.append(connection.to_pin)
            else:
                raise ParserError(f'Connection {connection} duplicates input '
                                  f'of pin {connection.to_pin}. Check your connections')


class _RecipeItem(dict):
    def __init__(self, required_data, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for data_name, data_type in required_data.items():
            data_value = kwargs.get(data_name)
            if data_value is None:
                print(data_value)
                raise ParserError(f'No {data_name} for node in: {kwargs}')

            if not isinstance(data_value, data_type):
                raise ParserError(f'{data_name} should be {data_type}, not {type(data_value)}')

        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    self[k] = v

        if kwargs:
            for k, v in kwargs.items():
                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super().__delitem__(key)
        del self.__dict__[key]


class _NodeRecipeItem(_RecipeItem):
    def __init__(self, **kwargs):
        required_data = {
            'id': object,
            'name': str,
            'plugin_name': str,
            'parameters': dict
        }
        super().__init__(required_data, **kwargs)


class _ConnectionRecipeItem(_RecipeItem):
    def __init__(self, **kwargs):
        required_data = {
            'name': str,
            'from_pin': _RecipeItem,
            'to_pin': _RecipeItem
        }

        pin_data = {
            'node': object,
            'pin': str
        }

        for attribute in ('from_pin', 'to_pin'):
            kwargs[attribute] = _RecipeItem(pin_data, **kwargs[attribute])

        super().__init__(required_data, **kwargs)
