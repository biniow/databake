#!/usr/bin/env python
# -*- coding: utf-8 -*-
from databake.lib.graph.exceptions import NodeError
from databake.lib.graph.pin import INPUT_PIN, OUTPUT_PIN, Pin


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
