#!/usr/bin/env python
# -*- coding: utf-8 -*-
import importlib
from databake.lib.graph.exceptions import NodeError
from databake.lib.graph.pin import INPUT_PIN, OUTPUT_PIN, Pin


class Node:
    def __init__(self, node_id, plugin_name, name='Node', parameters=None, auto_import=False):
        self.node_id = node_id
        self.name = name
        self.plugin_name = plugin_name
        self.level = 0

        self.input_pins = []
        self.output_pins = []
        self.parameters = {}

        if parameters:
            self.parameters = parameters

        if auto_import:
            self.import_config_from_plugin()

    def __str__(self):
        return f'Node:{self.name}({self.node_id})'

    def add_pin(self, pin):
        if not isinstance(pin, Pin):
            raise TypeError(f'{type(pin)} is not supported')

        if pin in self.input_pins + self.output_pins:
            raise NodeError(f'{pin} is already associated with {self}')

        if pin.type == INPUT_PIN:
            self.input_pins.append(pin)
        elif pin.type == OUTPUT_PIN:
            self.output_pins.append(pin)

        pin.node = self

    def remove_pin(self, pin):
        for pins_list in (self.input_pins, self.output_pins):
            if pin in pins_list:
                pins_list.remove(pin)
                break
        else:
            raise NodeError(f'{pin} does not exists in {self}')

    def import_config_from_plugin(self):
        plugin = importlib.import_module(self.plugin_name)
        self._iterate_plugin_pins(plugin.__input_pins__, INPUT_PIN)
        self._iterate_plugin_pins(plugin.__output_pins__, OUTPUT_PIN)

        for param_name, param_type in plugin.__parameters__.items():
            valid_types = (param_type, type(None))
            if not isinstance(self.parameters.get(param_name), valid_types):
                raise NodeError(f'Invalid type of {param_name} parameter. Should be {param_type}')

    def _iterate_plugin_pins(self, pins, pin_type):
        for pin in pins:
            self._add_pin_wrapper(pin, pin_type)

    def _add_pin_wrapper(self, pin_name, pin_type):
        pin = Pin(pin_name, pin_type)
        self.add_pin(pin)