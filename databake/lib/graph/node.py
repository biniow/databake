#!/usr/bin/env python
# -*- coding: utf-8 -*-
import warnings

from databake.lib.graph.exceptions import InvalidPinTypeError
from databake.lib.graph.pin import Pin, INPUT_PIN, OUTPUT_PIN, PIN_TYPES


class Node:
    def __init__(self, node_id, plugin, name='Node'):
        self.node_id = node_id
        self.name = name
        self.level = 0
        self.input_pins = []
        self.output_pins = []
        self.options = {}
        self.plugin = plugin

    def __str__(self):
        return f'Node:{self.name}({self.node_id})'

    def add_pin(self, name, pin_type):
        if pin_type not in PIN_TYPES:
            raise InvalidPinTypeError

        pin = Pin(self, name, pin_type)

        if pin in self.input_pins + self.output_pins:
            warnings.warn(f'{pin} is already associated with {self}')
            return pin

        if pin_type == INPUT_PIN:
            self.input_pins.append(pin)
        elif pin_type == OUTPUT_PIN:
            self.output_pins.append(pin)

        return pin


